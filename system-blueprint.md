# VeriSphere Full System Blueprint (Protocol + App + Business Logic)
Version: 0.2-draft
Format: ASCII-only Markdown

This document describes the full VeriSphere MVP system design, split into:

- Core on-chain protocol (EVM, Avalanche)
- Application layer (backend, UI, AI helpers)
- Business and operational logic

All non-on-chain data (external URLs, files, images, comments, identities)
is treated as "discussion material" only, similar to Quora threads or
Wikipedia talk pages. It may guide users but never overrides on-chain rules.

-------------------------------------------------------------------------------
1. High-Level Overview
-------------------------------------------------------------------------------

VeriSphere is a truth-staking game and protocol:

- Claims are represented as immutable Posts on-chain.
- Players stake VSP either in support of or in challenge to Posts.
- Over time, stakes grow or shrink based on how well each Post aligns
  with the emergent Verity Score (VS) and the overall stake distribution.
- Links between Posts create a graph of supporting and challenging claims.
- Off-chain services provide semantic deduplication, decomposition,
  discovery, and discussion UI, but do not change protocol state.

Layers:

1. Protocol layer (on-chain)
   - VSP token
   - Authority
   - PostRegistry
   - StakeEngine
   - LinkGraph
   - ScoreEngine

2. Application layer (off-chain)
   - API gateway
   - Indexer and database
   - AI services for semantic search, duplicate detection, claim decomposition
   - Web and mobile clients
   - Identity and profiles
   - Evidence, discussions, and external references

3. Operations and business layer
   - Bounty system and rewards
   - Governance processes
   - Optional VeriSphere Foundation site

-------------------------------------------------------------------------------
2. Protocol Layer (On-Chain)
-------------------------------------------------------------------------------

2.1 Core Principles

- On-chain structures and rules are minimal and deterministic.
- All economic consequences (mint / burn / staking rewards) are driven
  by on-chain data only.
- Off-chain components can suggest, summarize, and assist, but they
  cannot override protocol rules.
- Posts, stakes, and links form the canonical "truth graph" of the system.

2.2 Components

- VSPToken: ERC-20 token with controlled mint / burn and ERC-2612 permit.
- Authority: Role system controlling who may mint or burn.
- PostRegistry: Manages Posts (claims and links). Burns posting fees on
  creation. Enforces case-insensitive whitespace-normalized claim
  deduplication.
- LinkGraph: Stores directed evidence edges. Rejects self-loops and
  duplicate edges. Cycles are permitted at the storage layer; cycle
  handling is performed in the ScoreEngine (Section 2.3).
- StakeEngine: Manages consolidated per-user stake lots, snapshot-based
  growth and decay, and sMax tracking.
- ScoreEngine: Computes base and effective Verity Scores with stake-
  weighted propagation, recursion-stack cycle detection, and
  governance-bounded fan-in.

2.3 Post Object and Link Semantics

Posts have two content types: Claim and Link. A Claim stores text. A
Link stores (fromPostId, toPostId, isChallenge) and triggers an edge
insertion in LinkGraph. The post itself (whether claim or link) is
the staking target; users stake on a Post by its post ID.

Key rules:

- A claim's text is an atomic assertion (single claim).
- Posts are immutable once created.
- Claim post IDs start at 1; 0 is reserved as a null sentinel.
- Links between two claims with identical (from, to, isChallenge) are
  rejected as duplicates. Self-loops (from == to) are rejected.
- Links themselves are Posts and can be staked on like any other Post.
- The link graph permits cycles. The LinkGraph contract does not
  enforce a DAG. Score computation handles cycles in the ScoreEngine
  via a stack-based detection mechanism (any post already on the
  recursion stack contributes 0 for that path) and a hard depth limit
  of 32 as additional safety.
- The ScoreEngine bounds incoming-edge processing per claim and
  outgoing-link summation per parent (both default to 64,
  governance-configurable). When a claim or parent exceeds its limit,
  edges are sorted by link stake descending — with ties broken by
  linkPostId ascending — and only the top-N participate. Lower-staked
  edges beyond the cap are inert: they neither contribute to the
  parent's denominator nor produce a numerator, preserving
  conservation of influence (whitepaper §4.4) under bounded fan-out.
  Off-chain indexers must apply the same sort-and-cap rule with the
  same tiebreak when recomputing scores.

2.4 Staking Model (Summary)

The StakeEngine maintains per-(post, side) consolidated stake lots.
At most one lot per user per side per post exists at any time. The
contract enforces single-sided positions: a user with stake on the
support side of a post cannot add a challenge stake on the same post
(reverts with `OppositeSideStaked`); they must withdraw fully and
re-enter on the other side.

Each StakeLot represents a user's consolidated position:

    struct StakeLot {
        address staker;
        uint256 amount;             // current amount (post-snapshot)
        uint8   side;               // 0 = support, 1 = challenge
        uint256 weightedPosition;   // stake-weighted queue position
        uint256 entryEpoch;         // epoch of first stake on this side
    }

When a user adds stake to an existing lot, the lot's `amount` grows
in place and the StakeEngine recomputes every lot's `weightedPosition`
on that side as the midpoint of its share of the new side total:

    weightedPosition = cumBefore + amount / 2

where `cumBefore` is the running sum of the amounts of lots earlier
in the array. Earlier-entered users retain their array slot, so a
top-up enlarges the lot in place rather than moving the user to the
back of the queue. (Because every lot's `cumBefore` shifts when any
lot's `amount` changes, all positions on the side are recomputed
together; the relative array order is preserved.)

Per side queue:

    struct SideQueue {
        StakeLot[] lots;
        uint256 total;        // sum of amounts on this side
    }

Per post:

    struct PostState {
        SideQueue[2] sides;            // [0] support, [1] challenge
        uint256      lastSnapshotEpoch;
        // user => lots index + 1 (per side)
    }

Global StakeEngine state:

- sMax: a moving reference for the largest post total. Tracked via
  a top-3 list of (postId, total). Whenever the tracker is updated and
  at least one entry has a non-zero total, sMax is snapped directly
  to the leader's total — there is no slow decay during normal
  operation. A fallback exponential decay (governance-configurable;
  currently 10% per epoch capped at 30 epochs) is applied only when
  the tracker is empty (no active posts), which prevents a stale sMax
  from staying frozen forever after a complete unwind.
- snapshotPeriod: minimum elapsed time between O(N) per-post
  recomputations. Defaults to 1 day; governance-configurable.
- (Earlier StakeEngine versions exposed a `numTranches` storage
  variable; the v3 implementation deployed today removed it entirely.
  Position weighting is continuous via the midpoint formula above.)

Activity threshold:

- A post is "active" when its total stake is at or above the
  ClaimActivityPolicy threshold. Inactive posts contribute nothing
  to other posts' effective VS.

2.5 Snapshot-Based Growth and Decay

Note: The normative specification of stake economics is in
claim-spec-evm-abi.md, Appendix A. This section provides an
overview; the appendix governs in case of conflict.

Time is divided into epochs of one day. Per-post recomputation
("snapshot") runs at most once per snapshotPeriod, triggered by any
stake/withdraw on that post or by an explicit `updatePost(postId)`
call (permissionless). Between snapshots, view functions project
unrealized gains and losses lazily so that reads always reflect the
current state without writing to storage.

Verity Score (base) used by the StakeEngine:

- Let A = support total, D = challenge total, T = A + D.
- If T == 0, sMax == 0, or 2A == T (perfectly balanced), the snapshot
  is economically neutral and only the lastSnapshotEpoch is bumped.
- Otherwise:

      vsNum = 2A - T            (signed)
      supportWins = vsNum > 0
      absVS = abs(vsNum)
      vRay  = absVS * RAY / T
      participationRay = T * RAY / sMax

Per-epoch effective base rate:

      rMin = R_MIN_ANNUAL_RAY * EPOCH_LENGTH * epochsElapsed / YEAR
      rMax = R_MAX_ANNUAL_RAY * EPOCH_LENGTH * epochsElapsed / YEAR
      rBase = rMin + (rMax - rMin) * vRay * participationRay / RAY^2

Per-lot growth/decay (continuous midpoint weighting; no side-wide
budget redistribution):

For each lot on the side:

      posShare    = lot.weightedPosition * RAY / sideTotal       (clamped to RAY)
      posWeight   = RAY - posShare
      delta       = lot.amount * rBase * posWeight / RAY^2

If the lot is on the winning side (aligned):

      lot.amount += delta              (StakeEngine mints delta)

If the lot is on the losing side (opposed):

      loss = min(delta, lot.amount)
      lot.amount -= loss               (StakeEngine burns loss)

Side totals are then recomputed by summing lot amounts. Lot amounts
never go below zero (limited liability).

Notes:

- Each lot's effective per-epoch rate is its own
  `rBase * posWeight / RAY`, applied to its own amount, with no
  proportional-share normalization across the side. A sole staker
  earns `rBase / 2`; the first of many earlier stakers approaches
  `rBase`. An individual lot's rate never exceeds rBase.
- sMax tracking uses a top-3 leader tracker that snaps `sMax` to the
  current leader's total whenever any post is active. A fallback
  exponential decay (governance-configurable; currently 10% per epoch
  capped at 30 epochs) only runs when no active posts exist.
- The model discourages "fracturing" into many small posts: small T
  relative to sMax yields low participation, hence low rate.

2.6 Staking API (Simplified)

StakeEngine exposes:

- stake(postId, side, amount):
  - Reverts if the user has any stake on the opposite side.
  - Pulls amount of VSP via transferFrom.
  - Either creates a new lot at the back of the queue or merges into
    the user's existing lot (stake-weighted position update).
  - May trigger a snapshot if the snapshot period has elapsed.
  - Updates sMax via the top-3 tracker.

- withdraw(postId, side, amount, lifo):
  - The lifo parameter is deprecated and ignored; kept for ABI
    compatibility.
  - May trigger a snapshot first (materializing gains/losses).
  - Reduces the caller's lot amount and recomputes every lot's
    weightedPosition on the side using the midpoint formula. A
    fully-withdrawn user keeps their array slot as a ghost lot
    (`amount = 0`); ghost lots are removable by a governance call
    to compactLots(postId, side).
  - Updates sMax via the top-3 tracker.

- setStake(postId, target):
  - Signed-target convenience entrypoint used by the application
    layer. `target == 0` withdraws any stake on either side;
    `target > 0` withdraws any challenge stake then sets support to
    `|target|` (adding or removing as needed); `target < 0` does the
    opposite. All effects happen in a single transaction.

- updatePost(postId):
  - Permissionless. Forces a snapshot if any time has elapsed since
    the last one. Cheap when called multiple times in the same epoch
    (early return).

2.7 VSP Token and Authority

VSPToken:

- ERC-20 with ERC-2612 permit and UUPS upgradeability.
- Mint and burn gated by Authority roles.

Authority:

- owner (governance)
- minters
- burners

Main relationships:

- StakeEngine holds the minter and burner roles. It mints VSP into
  itself for winning lots and burns VSP from its own balance for
  losing lots.
- The PostRegistry holds the burner role for posting fee burns; it
  pulls VSP from the user via transferFrom and immediately burns it.

-------------------------------------------------------------------------------
3. Application Layer (Off-Chain)
-------------------------------------------------------------------------------

3.1 Core Principle: Discussion Material

All off-chain data is "discussion material":

- User profiles, display names, avatars.
- Long-form reasoning, arguments, comments.
- External links to articles, PDFs, videos, images.
- Summaries, AI-generated explanations, and annotations.

The protocol does not read or trust this data directly. It is used to:

- Help humans discover and evaluate claims.
- Help humans decide where to stake on-chain.
- Provide context for reading the on-chain truth graph.

This is conceptually similar to:

- Quora threads discussing a question.
- Wikipedia talk pages behind an article.

3.2 Major Components

1. API Gateway
   - Serves UI and external tools.
   - Exposes read and write endpoints.
   - Does not bypass protocol; all state changes ultimately go through
     on-chain transactions.

2. Indexer
   - Listens to Avalanche logs.
   - Builds a relational or graph representation of:
     - Posts and their metadata.
     - Stakes and snapshot history.
     - Link relations from LinkGraph events.
   - Provides fast queries for UI and analytics.
   - When recomputing effective VS off-chain, must apply the same
     fan-in caps as the on-chain ScoreEngine to remain consistent.

3. Database
   - Stores:
     - Cached copies of on-chain data (for quick querying).
     - Off-chain discussion objects (comments, threads).
     - User profiles and display names.
     - Evidence records (references to external URLs, IPFS hashes).
     - AI annotations and semantic features.

4. AI Services
   - Semantic duplicate detection.
   - Claim decomposition (enforcing atomicity in the UI).
   - Suggests related Posts to avoid duplication.
   - Suggests possible evidence or counter-evidence.
   - Summarizes debates and stake dynamics.

5. Web and Mobile Clients
   - Present claims as canonical pages.
   - Show stake queues and truth pressure.
   - Provide forms for creating new Posts.
   - Provide forms for staking, challenging, and linking.

3.3 Identity and Profiles

Profiles are strictly off-chain:

- Users are identified primarily by wallet address (EOA).
- They may optionally create:
  - Display name (unique or scoped to the site).
  - Bio, avatar, links to external accounts.
- Future support for:
  - "Verified" badges (KYC or Web of Trust), purely off-chain.
  - Social graph interactions (follows, mutes), stored in the app DB.

Business rule:

- Profile and identity metadata never influence protocol-level staking
  or VS computation directly.
- The UI may re-order or highlight content based on profile attributes,
  but the protocol remains neutral.

3.4 Evidence and Discussion Model

Evidence:

- Off-chain object representing a reference:
  - URL (HTTP, IPFS, Arweave, etc.).
  - Local attachment (image, PDF).
- Stored in the app database with:
  - ID, URL, title, source, metadata.
  - Association to one or more Posts.
  - Optional AI-generated summary.

Discussion:

- Threaded comments attached to a Post:
  - commentId, parentId, author, body, timestamp.
- Semantically separate from the canonical claim text.
- No direct effect on the staking engine.

UI integration:

- Claim page shows:
  - On-chain claim text and VS / stake totals.
  - Evidence section with references.
  - Discussion section with comments.

3.5 Semantic Duplicate Detection and Atomicity

When a user attempts to create a new Post:

1. The app calls the semantic duplication service with the proposed text.
2. The service:
   - Embeds the text into a vector.
   - Compares against existing Posts.
   - Returns likely duplicates or near-duplicates.
3. The UI prompts the user:
   - "Similar claims exist. Do you want to stake on one of these instead?"
4. If the user insists, they can still create a new Post, but:
   - They may face a smaller participation factor if stake fractures
     across many similar posts.
   - The UI can mark the new Post as a "possible duplicate".

Note: the on-chain PostRegistry also enforces a strict, normalized
duplicate check (case-insensitive, whitespace-collapsed, trimmed)
that reverts with DuplicateClaim before any fee is charged. The
semantic service catches near-duplicates the on-chain check would
miss.

Atomicity:

- The claim decomposition service can:
  - Identify multi-assertion text.
  - Suggest splitting into multiple atomic claims.
  - Provide a UI to accept or adjust the split.
- The final atomic claims are the ones actually posted on-chain.

3.6 Backend Processes

Typical backend jobs:

- Snapshot tick:
  - For each Post with nonzero stake whose snapshot period has
    elapsed, call updatePost(postId) on-chain (or in batches).
- Indexing:
  - Continuously sync new blocks.
  - Update DB with new Posts and stakes.
- Analytics:
  - Compute trending Posts by:
    - Net stake delta.
    - VS changes.
    - New high-participation posts.
- Cleanup:
  - Archive or compress old logs.
  - Maintain search indices.

-------------------------------------------------------------------------------
4. Business Logic and Foundation
-------------------------------------------------------------------------------

4.1 Governance and Bounties

Governance lives largely off-chain (GitHub, Google Sheets) but is wired
to on-chain treasury contracts and bounties.

High-level flow:

- Tasks are defined as GitHub issues (docs repo).
- Each issue has:
  - Phase, task name, description.
  - Estimated hours.
  - Bounty in VSP.
  - Status labels.
- A CI workflow syncs issue states to a Google Sheet.
- Upon completion:
  - Maintainers approve the work.
  - A treasury contract pays out VSP to the contributor wallet.
- The reward curve favors early work (pre-MVP) more than late work.

4.2 VeriSphere Foundation Site

An optional foundation site (for example, verisphere.org) may:

- Host the main web client.
- Provide documentation, FAQs, and onboarding.
- Present governance and treasury transparency.
- Run the official indexer and APIs.

Business model ideas (non-protocol, optional):

- Grants and donations.
- Integration services and enterprise features.
- Analytics dashboards and premium tools.
- Optional hosted APIs with rate limits and service guarantees.

Important:

- The foundation is not required for the protocol to function.
- Anyone can run their own indexer, API gateway, and UI.
- The foundation cannot censor or alter protocol state.

4.3 Incentive Alignment

Players:

- Earn by staking correctly on canonical Posts and links.
- Lose by staking incorrectly or on weak, fractured Posts.

Builders:

- Earn bounties for advancing the protocol and ecosystem.
- Gain reputation by building open-source tooling.

Operators:

- Can run their own frontends and services.
- Benefit from traffic and integrations.

4.4 Risks and Mitigations

Spam and low-quality claims:

- On-chain posting fee enforces minimal cost.
- UI can de-emphasize Posts with little stake or high duplication.

Sybils:

- Economic costs for meaningful influence.
- App layer can add soft identity checks if desired.
- Note: lot consolidation prevents one user from gaming position
  weight by splitting into many lots, but does not prevent a user
  from spreading stake across multiple wallets. Sybil resistance at
  the wallet level is an open application-layer concern.

Centralization:

- Multiple independent frontends are encouraged.
- Public APIs and open data formats for indexer output.

-------------------------------------------------------------------------------
5. Summary
-------------------------------------------------------------------------------

- Protocol layer:
  - Defines Posts, stakes, and links via PostRegistry, StakeEngine,
    LinkGraph, and ScoreEngine.
  - Stakes are consolidated per (user, post, side) with stake-weighted
    position averaging on additions; positions cannot be split, and a
    user cannot hold both sides on the same post.
  - Assigns economic outcomes through snapshot-based growth and decay,
    with continuous position weighting.
  - Uses a top-3 sMax tracker that snaps to the leader's total during normal operation; a fallback exponential decay only runs when no posts are active
    on large posts without permanently suppressing later participation.
  - Permits cycles in the link graph; safety is achieved by recursion-
    stack cycle detection plus a depth-32 cap and bounded fan-in in
    the ScoreEngine.

- Application layer:
  - Treats all off-chain data as discussion material only.
  - Provides identity, profiles, evidence, and comments like Quora or
    Wikipedia talk pages.
  - Offers AI helpers for duplicate detection and claim decomposition.

- Business logic:
  - Bounty-driven early development.
  - Optional foundation hosting an official frontend and API.
  - Open ecosystem for additional clients and services.

Together, these layers create an adversarial, economically grounded
truth-staking environment where beliefs have consequences, but discussion,
context, and evidence remain free-form and off-chain.
