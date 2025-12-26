# VeriSphere Full System Blueprint (Protocol + App + Business Logic)
Version: 0.1-draft
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

- VSPToken: ERC-20 compatible token with controlled mint / burn.
- Authority: Simple role system controlling who may mint or burn.
- PostRegistry: Manages Posts and link structure (via targetPostId).
- StakeEngine: Manages staking queues and epoch-based growth/decay.
- (Future) LinkGraph: Optional separate contract for more complex link
  semantics; MVP can encode links via targetPostId and side.

2.3 Post Object and Link Semantics

Post structure (conceptual):

    struct Post {
        address creator;
        uint256 timestamp;
        string text;
        int256 targetPostId;    // 0 = not a link
                                // >0 = link to that post (support)
                                // <0 = link to abs(targetPostId) (challenge)
        uint256 supportTotal;   // optional, derived in StakeEngine / indexer
        uint256 challengeTotal; // optional, derived in StakeEngine / indexer
    }

Key rules:

- text is an atomic assertion (single claim).
- Posts are immutable once created.
- If targetPostId == 0, the Post is a "root claim".
- If targetPostId > 0, the Post is interpreted as a supporting link to
  Post targetPostId.
- If targetPostId < 0, the Post is interpreted as a challenging link to
  Post abs(targetPostId).
- Links themselves can be staked on like any other Post.
- Circular references are prevented at the application layer and/or
  in any future LinkGraph contract.

Note: For gas and storage efficiency, supportTotal and challengeTotal
may be tracked in StakeEngine instead of PostRegistry, or omitted from
storage and computed off-chain by indexers.

2.4 Staking Model (Summary)

The StakeEngine maintains per-post queues of "StakeLots" on both sides
(support and challenge).

Each StakeLot represents a single staking action:

    struct StakeLot {
        address staker;
        uint256 amount;
        uint8   side;         // 0 = support, 1 = challenge
        uint256 begin;        // queue position start (global from last toward first)
        uint256 end;          // queue position end
        uint256 mid;          // (begin + end) / 2
        uint256 entryEpoch;   // epoch at which this lot was created
    }

Per post:

    struct SideQueue {
        StakeLot[] lots;
        uint256 total;        // sum of amounts on this side
    }

    struct PostState {
        SideQueue[2] sides;   // [0] support, [1] challenge
        uint256 lastUpdatedEpoch;
    }

Global:

- sMax: maximum total stake across all posts ever seen (monotonic nondecreasing).
- postingFeeThreshold: if total stake T on a post is below this, VS does not drive economics.

2.5 Epoch-Based Growth and Decay

Time is divided into discrete epochs:

- EPOCH_LENGTH = 1 day (governance-tunable).
- Each Post has lastUpdatedEpoch. When updatePost(postId) is called:
  - Compute how many epochs have elapsed.
  - Apply growth or decay for support and challenge lots based on:
    - Verity Score (VS) sign and magnitude.
    - Post size relative to sMax.
    - Lot queue position (mid) relative to sMax.

Verity Score (base):

- Let A = support total, D = challenge total, T = A + D.
- If T == 0 or T < postingFeeThreshold, treat as neutral (no economic effect).
- VS is conceptually:

      VS = (2 * A / T - 1) * 100

- Only the sign and magnitude drive economics in StakeEngine.

Post size factor:

- T is total stake on this post.
- sMax is global max T seen so far across all posts.
- x = T / sMax.
- A clamped post factor P is:

      P_raw = x
      P = clamp(P_raw, P_min, P_max)

  where P_min and P_max are governance parameters in ray units (1e18).

Per-epoch effective rate:

- Annual min and max rates:

      R_MIN_ANNUAL (ray)
      R_MAX_ANNUAL (ray)

- For epochsElapsed:

      rMinEpoch = R_MIN_ANNUAL * EPOCH_LENGTH * epochsElapsed / YEAR_IN_SECONDS
      rMaxEpoch = R_MAX_ANNUAL * EPOCH_LENGTH * epochsElapsed / YEAR_IN_SECONDS
      rSpanEpoch = max(rMaxEpoch - rMinEpoch, 0)

- Verity magnitude:

      vRay = abs(2A - T) * 1e18 / T

- Effective rate (ray):

      rEff = rMinEpoch + (rSpanEpoch * vRay * P) / 1e36

Positional weight and per-lot rate:

- Each lot has mid position in the queue, from 0 up to T.
- Global normalization uses sMax:

      wRay = lot.mid * 1e18 / sMax

- If wRay is small, the lot is "late"; if wRay is large, the lot is "early"
  in the largest possible context.
- Side alignment:
  - If supportWins and lot side is support: aligned
  - If challengeWins and lot side is challenge: aligned
  - Otherwise: misaligned

- Per-lot absolute rate:

      rUserAbs = rEff * wRay / 1e18

- Growth or decay:

      delta = lot.amount * rUserAbs / 1e18

      if aligned:
          lot.amount += delta
      else:
          lot.amount = max(lot.amount - delta, 0)

Notes:

- sMax is not decreased when queues shrink; it only ever grows.
- This ensures that early stakes on large posts keep a strong positional weight.
- The model discourages "fracturing" into many small posts because those posts
  will have small T relative to sMax, and thus lower effective P.

2.6 Staking API (Simplified)

StakeEngine exposes:

- stake(postId, side, amount):
  - Pulls amount of VSP from the user via transferFrom.
  - Appends a StakeLot for that post and side.
  - Recomputes begin, end, mid for that side and updates T and sMax.

- withdraw(postId, side, amount, lifo):
  - Withdraws amount from the caller's lots on that side.
  - lifo chooses whether to draw from last lots first or first lots first.
  - After withdrawal, recomputes begin, end, mid and totals for that side.

- updatePost(postId):
  - Applies epoch growth/decay to all StakeLots for that post.
  - Updates PostState.lastUpdatedEpoch.

2.7 VSP Token and Authority

VSPToken:

- Standard ERC-20 interface.
- Controlled mint and burn via Authority.

Authority:

- owner
- minters
- burners

Main relationships:

- StakeEngine will, in a full rollout, mint and burn VSP to realize
  the economic growth or decay of stakes (MVP may simulate by internal
  accounting first).
- Other protocol modules (governance, treasury) can also mint/burn
  under Authority.

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
     - Stakes and epoch history.
     - Link relations derived from targetPostId.
   - Provides fast queries for UI and analytics.

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
   - They may face a smaller P factor if stake fractures across many similar posts.
   - The UI can mark the new Post as a "possible duplicate".

Atomicity:

- The claim decomposition service can:
  - Identify multi-assertion text.
  - Suggest splitting into multiple atomic claims.
  - Provide a UI to accept or adjust the split.
- The final atomic claims are the ones actually posted on-chain.

3.6 Backend Processes

Typical backend jobs:

- Epoch tick:
  - For each Post with nonzero stake and that has not been updated this epoch:
    - Call updatePost(postId) on-chain (or in batches).
- Indexing:
  - Continuously sync new blocks.
  - Update DB with new Posts and stakes.
- Analytics:
  - Compute trending Posts by:
    - Net stake delta.
    - VS changes.
    - New high P posts.
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

Centralization:

- Multiple independent frontends are encouraged.
- Public APIs and open data formats for indexer output.

-------------------------------------------------------------------------------
5. Summary
-------------------------------------------------------------------------------

- Protocol layer:
  - Defines Posts, stakes, and link semantics via targetPostId.
  - Assigns economic outcomes through epoch-based growth and decay.
  - Uses a global sMax and per-lot mid positions to favor early stakes
    on large Posts.

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
