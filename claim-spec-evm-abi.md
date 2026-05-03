# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.7 (MVP, ASCII only, link-aware, v3 StakeEngine, v2.1 ScoreEngine)

This document defines the ABI-level specification for the core VeriSphere
on-chain components:

- PostRegistry
- StakeEngine
- LinkGraph
- VSPToken (subset)
- Authority (subset)

The main body is pure ABI (interfaces, structs, events, errors).
All economic and behavioral explanations are in the appendices.

------------------------------------------------------------------------------
1. Core Data Structures
------------------------------------------------------------------------------

Note: These structs are conceptual. Actual storage layout and packing may vary.

## 1.1 Post

A Post is an atomic claim or a link between two claims.

struct Post {
    address creator;
    uint256 timestamp;
    ContentType contentType;  // 0 = Claim, 1 = Link
    uint256 contentId;        // index into claims[] or links[] array
    uint256 creationFee;      // VSP burned on creation
}

## 1.2 StakeLot

A StakeLot is a consolidated staking position — one per user per side
per post. When a user stakes additional tokens on a side where they
already have a lot, the existing lot is merged (see Appendix A.2).

struct StakeLot {
    address staker;
    uint256 amount;
    uint8   side;              // 0 = support, 1 = challenge
    uint256 weightedPosition;  // stake-weighted queue coordinate
    uint256 entryEpoch;        // epoch when lot was first created
}

## 1.3 Link

A Link is an explicit directed edge between two claims, stored in both
PostRegistry (as a Link struct) and LinkGraph (as adjacency lists).

struct Link {
    uint256 fromPostId;     // evidence provider (outgoing end)
    uint256 toPostId;       // evidence receiver (incoming end)
    bool    isChallenge;    // true = from challenges to; false = from supports to
}

The link graph permits cycles. The LinkGraph contract does not enforce
acyclicity; cycle handling is performed by the ScoreEngine at read time
(see Appendix C).

------------------------------------------------------------------------------
2. IPostRegistry ABI
------------------------------------------------------------------------------

interface IPostRegistry {
    // Create a new immutable claim.
    // text           Claim text, expected to be atomic and non-empty.
    //                Max length: 2000 bytes (PostRegistry.MAX_CLAIM_LENGTH).
    //                Deduplicated via case-insensitive, whitespace-normalized
    //                keccak256 hash. Reverts DuplicateClaim(existingPostId)
    //                if a matching claim already exists.
    // Returns        Newly assigned postId.
    function createClaim(string calldata text)
        external
        returns (uint256 postId);

    // Create a link between two claims.
    // fromPostId     The claim providing evidence (outgoing end).
    // toPostId       The claim receiving evidence (incoming end).
    // isChallenge    True if from challenges to; false if from supports to.
    // Both posts must exist and be claims (not links).
    // Reverts DuplicateLink if the same (from, to, isChallenge) already exists.
    // Returns        Newly assigned postId for the link post.
    function createLink(
        uint256 fromPostId,
        uint256 toPostId,
        bool isChallenge
    ) external returns (uint256 postId);

    // Read a post by id.
    function getPost(uint256 postId)
        external
        view
        returns (Post memory);

    function getClaim(uint256 claimId) external view returns (string memory);
    function getLink(uint256 linkId) external view returns (Link memory);

    // Check if a claim with this text already exists on-chain.
    // Returns existingPostId, or type(uint256).max if not found.
    function findClaim(string calldata text)
        external
        view
        returns (uint256 existingPostId);

    // Events
    event PostCreated(uint256 indexed postId, address indexed creator, ContentType contentType);
    event FeeBurned(uint256 indexed postId, uint256 feeAmount);

    // Errors
    error InvalidClaim();
    error ClaimTooLong(uint256 length, uint256 max);
    error DuplicateClaim(uint256 existingPostId);
    error DuplicateLink(uint256 fromPostId, uint256 toPostId, bool isChallenge);
    error FromPostDoesNotExist();
    error ToPostDoesNotExist();
    error FromPostMustBeClaim();
    error ToPostMustBeClaim();
}

------------------------------------------------------------------------------
3. IStakeEngine ABI
------------------------------------------------------------------------------

interface IStakeEngine {
    // ─── User entrypoints ────────────────────────────────────────

    // Stake VSP on a post, on either support or challenge side.
    // Reverts OppositeSideStaked if user already has stake on the other side.
    function stake(uint256 postId, uint8 side, uint256 amount) external;

    // Withdraw stake from a post. Reduces the user's consolidated lot.
    // lifo parameter is accepted for ABI compatibility but ignored.
    // Recomputes weightedPosition for every lot on the side after the
    // withdrawal (midpoint formula) — partial withdrawal therefore
    // shifts the user toward the front of the queue. A fully-withdrawn
    // user retains a ghost lot (amount = 0) until compactLots is called.
    function withdraw(uint256 postId, uint8 side, uint256 amount, bool lifo) external;

    // Convenience entrypoint: set the user's stake on a post to a
    // signed target value, atomically.
    //   target == 0  : withdraw all stake on either side
    //   target > 0   : withdraw any challenge stake, then set support to |target|
    //   target < 0   : withdraw any support stake, then set challenge to |target|
    function setStake(uint256 postId, int256 target) external;

    // Apply epoch growth/decay. Anyone may call; typically a keeper or backend.
    function updatePost(uint256 postId) external;

    // ─── Read methods ────────────────────────────────────────────

    // Returns projected totals (includes unrealized gains/losses).
    function getPostTotals(uint256 postId)
        external view returns (uint256 support, uint256 challenge);

    // Returns projected user stake (includes unrealized gains/losses).
    function getUserStake(address user, uint256 postId, uint8 side)
        external view returns (uint256);

    // Returns lot diagnostics for a (user, post, side):
    //   amount, weightedPosition, entryEpoch, sideTotal, positionWeight (RAY).
    function getUserLotInfo(address user, uint256 postId, uint8 side)
        external view returns (
            uint256 amount,
            uint256 weightedPosition,
            uint256 entryEpoch,
            uint256 sideTotal,
            uint256 positionWeight
        );

    // Returns the top-3 sMax tracker (postId, total) tuples.
    function getTopPosts() external view returns (
        uint256 p0, uint256 t0,
        uint256 p1, uint256 t1,
        uint256 p2, uint256 t2
    );

    // ─── Governance ──────────────────────────────────────────────

    // Set the snapshot period (minimum gap between O(N) per-post updates).
    function setSnapshotPeriod(uint256 newPeriod) external;

    // Set the sMax fallback decay rate. Must be in (0, RAY].
    // RAY (1e18) = no decay; smaller values decay faster.
    function setSMaxDecayRate(uint256 newRate) external;

    // Set the cap on the number of fallback-decay epochs projected
    // in a single call (gas safety for stale sMax catch-up).
    function setSMaxDecayMaxEpochs(uint256 newMax) external;

    // Rebuild the top-3 sMax tracker from a candidate list of postIds.
    // Useful if the tracker has gone stale (e.g. after large withdrawals
    // by the previous leader).
    function rescanSMax(uint256[] calldata postIds) external;

    // Remove zero-amount ghost lots. Governance-only.
    function compactLots(uint256 postId, uint8 side) external;

    // ─── Events ──────────────────────────────────────────────────

    event StakeAdded(uint256 indexed postId, address indexed staker, uint8 side, uint256 amount);
    event StakeWithdrawn(uint256 indexed postId, address indexed staker, uint8 side, uint256 amount, bool lifo);
    event PostUpdated(uint256 indexed postId, uint256 epoch, uint256 supportTotal, uint256 challengeTotal);
    event EpochMinted(uint256 indexed postId, uint256 amount);
    event EpochBurned(uint256 indexed postId, uint256 amount);
    event PositionsRescaled(uint256 indexed postId, uint8 side, uint256 oldMax, uint256 newCeiling);
    event LotsCompacted(uint256 indexed postId, uint8 side, uint256 removed);
    event SnapshotPeriodSet(uint256 oldPeriod, uint256 newPeriod);
    event SMaxRescanned(uint256 newSMax, uint256 newSMaxPostId);
    event SMaxDecayRateSet(uint256 oldRate, uint256 newRate);
    event SMaxDecayMaxEpochsSet(uint256 oldMax, uint256 newMax);

    // ─── Errors ──────────────────────────────────────────────────

    error InvalidSide();
    error AmountZero();
    error OppositeSideStaked();
    error NotEnoughStake();
    error ZeroAddressToken();
    error InvalidSnapshotPeriod();
    error NoGhostLots();
    error InvalidDecayRate();
    error InvalidDecayMaxEpochs();
}

------------------------------------------------------------------------------
4. ILinkGraph ABI
------------------------------------------------------------------------------

interface ILinkGraph {
    // Called by PostRegistry when a link is created.
    function addEdge(
        uint256 fromClaimPostId,
        uint256 toClaimPostId,
        uint256 linkPostId,
        bool isChallenge
    ) external;

    function getOutgoing(uint256 claimPostId) external view returns (Edge[] memory);
    function getIncoming(uint256 claimPostId) external view returns (IncomingEdge[] memory);
    function hasEdge(uint256 fromClaimPostId, uint256 toClaimPostId, bool isChallenge)
        external view returns (bool);

    // Events
    event EdgeAdded(uint256 indexed from, uint256 indexed to, uint256 indexed linkPostId, bool isChallenge);

    // Errors
    error SelfLoop();
    error DuplicateEdge(uint256 fromClaimPostId, uint256 toClaimPostId, bool isChallenge);
}

------------------------------------------------------------------------------
5. IVSPToken ABI (subset)
------------------------------------------------------------------------------

interface IVSPToken {
    function mint(address to, uint256 amount) external;
    function burn(uint256 amount) external;
    function burnFrom(address from, uint256 amount) external;
}

------------------------------------------------------------------------------
6. IAuthority ABI (subset)
------------------------------------------------------------------------------

interface IAuthority {
    function owner() external view returns (address);
    function isMinter(address who) external view returns (bool);
    function isBurner(address who) external view returns (bool);
}

------------------------------------------------------------------------------
7. Versioning
------------------------------------------------------------------------------

- Specification name: claim-spec-evm-abi
- Version: 0.7-mvp-v3
- Chain target: Avalanche C-Chain / Subnet (EVM compatible)

------------------------------------------------------------------------------
Appendix A. Economic Model (Normative — Continuous Positional Weighting)
------------------------------------------------------------------------------

This appendix is the NORMATIVE specification of stake economics.
It supersedes all previous descriptions of rate formulas, positional
weighting, and sMax behavior in other documents. The whitepaper and
architecture documents defer to this appendix on economic details.

This appendix matches the deployed StakeEngine Solidity implementation.

A.1. Symbols

For a given post P:

- A        = support total (sum of all support lot amounts after last snapshot)
- D        = challenge total (sum of all challenge lot amounts after last snapshot)
- T        = A + D
- VS_num   = 2A - T  (signed; positive means support wins)
- v        = |VS_num| * RAY / T  (verity magnitude, ray-scaled)

Global:

- sMax              = global reference stake, decaying (see A.7)
- R_MIN_ANNUAL      = governance-controlled minimum annual rate (ray, 1e18 = 100%)
- R_MAX_ANNUAL      = governance-controlled maximum annual rate (ray)
- EPOCH_LENGTH      = 1 day (86400 seconds)
- YEAR_LENGTH       = 365 days (31536000 seconds)
- RAY               = 1e18
- snapshotPeriod    = minimum time between O(N) snapshot updates (default 1 day)

Per StakeLot:

- amount             = current token amount (mutated by snapshots)
- weightedPosition   = stake-weighted queue coordinate (see A.2, A.5)
- side               = 0 (support) or 1 (challenge)
- entryEpoch         = epoch when lot was first created

A.2. Lot Consolidation

There is exactly one StakeLot per user per side per post. A user cannot
hold lots on both sides of the same post; attempting to stake on the
opposite side reverts with OppositeSideStaked.

When a user stakes additional tokens on a side where they already have
a lot, only the lot's amount changes — the lot keeps its array slot:

    existing.amount += newAmount

After every queue mutation (stake, top-up, withdrawal, snapshot), the
StakeEngine recomputes every lot's weightedPosition on the side as the
midpoint of its share of the side total:

    weightedPosition[i] = sum(amount[0..i-1]) + amount[i] / 2

That is, each lot's weightedPosition is the running cumulative-sum of
prior lots plus half of its own amount. Lots earlier in the array
therefore have lower weightedPosition values; topping up an existing
lot does not move the user to the back of the queue, but it does
expand the user's amount-weighted occupancy of the queue, which in
turn lowers the positionWeight of every lot behind them.

A fully-withdrawn user retains a "ghost lot" (amount = 0) at their
original array slot until governance calls compactLots(postId, side).
Ghost lots are skipped in epoch math (amount * anything = 0).

A.3. Base Verity Score

The StakeEngine computes VS internally using the symmetric formula:

    VS_num = 2A - T

If VS_num > 0, support wins. If VS_num < 0, challenge wins.
If VS_num == 0, no economic effect (neutral).

Note: The ScoreEngine (used for effective VS with link propagation)
uses a different, asymmetric formula:

    if A > D: baseVS = +(A * RAY / T)
    if D > A: baseVS = -(D * RAY / T)
    if A == D or T == 0: baseVS = 0

The StakeEngine formula and ScoreEngine formula agree on sign and on
the extremes (0, +/-RAY) but differ at intermediate values. This is
intentional: the StakeEngine needs only the sign and a magnitude for
rate computation, while the ScoreEngine needs a properly normalized
score for link propagation.

A.4. Participation Factor (Post Size)

The participation factor measures how significant this post's total
stake is relative to the global reference:

    participationRay = T * RAY / sMax

There is no clamping. The factor ranges from near 0 to RAY (or
above RAY transiently, though sMax is updated to at least T on every
interaction).

A.5. Epoch Rate Computation

Time is divided into discrete epochs of EPOCH_LENGTH seconds.
Snapshots are triggered at most once per snapshotPeriod by any
state-changing operation (stake, withdraw, or explicit updatePost).

For a snapshot spanning epochsElapsed epochs:

Step 1: Compute time-scaled rate bounds.

    rMin = R_MIN_ANNUAL * EPOCH_LENGTH * epochsElapsed / YEAR_LENGTH
    rMax = R_MAX_ANNUAL * EPOCH_LENGTH * epochsElapsed / YEAR_LENGTH

Step 2: Compute the base rate for this post.

    rBase = rMin + ((rMax - rMin) * vRay * participationRay) / (RAY * RAY)

Where vRay = |VS_num| * RAY / T (verity magnitude) and
participationRay = T * RAY / sMax (post size factor).

Properties:
- If VS_num == 0, the snapshot short-circuits: no lots are modified.
- If T == 0 or sMax == 0, no economic effect.
- rBase increases with both verity magnitude and post size.

A.6. Continuous Positional Weighting (Per-Lot Independent Rate)

Each lot's reward is determined independently by its weightedPosition
relative to the side total. There are no discrete buckets or tranches,
and there is no side-wide budget redistribution: every lot is
processed on its own.

    positionWeight = 1 - (lot.weightedPosition / sideTotal)
                   = (sideTotal - lot.weightedPosition) / sideTotal

Because weightedPosition is the midpoint of the lot's share of the
side total (A.2), a sole staker on a side has weightedPosition = T/2
and therefore positionWeight = 1/2; the first of many earlier stakers
has weightedPosition near 0 and approaches positionWeight = 1.0.

Per-lot epoch delta:

    delta = lot.amount * rBase * positionWeight / RAY

Note that delta scales as `amount * rBase * (T - wPos) / T`, so an
individual lot's effective per-epoch rate never exceeds rBase.

If aligned (lot side matches VS sign):
    lot.amount += delta       (StakeEngine mints delta into itself)
else:
    loss = min(delta, lot.amount)
    lot.amount -= loss        (StakeEngine burns loss; amount floored at 0)

Where "aligned" means:
- supportWins && lot.side == support, OR
- !supportWins && lot.side == challenge

The mint and burn totals are summed across all lots on both sides of
the post and a single VSP_TOKEN.mint and VSP_TOKEN.burn are issued
per snapshot (see A.9).

Note: The previous tranche-based model and its `numTranches` /
`setNumTranches` governance surface have been fully removed from the
deployed StakeEngine v3. The contract no longer has any tranche
storage or function; A.6 above is the entire reward math.

A.7. sMax Tracker and Fallback Decay

sMax is maintained via a top-3 post tracker. The tracker stores the
three (postId, total) tuples with the largest totals. Whenever any
post's total changes, the StakeEngine updates the tracker and snaps
sMax to the leader's total:

    if leaderTotal > 0:
        sMax = leaderTotal
        sMaxLastUpdatedEpoch = currentEpoch
    else:
        sMax = applyFallbackDecay(currentEpoch)

During normal operation — i.e., as long as at least one post has
non-zero total stake — sMax is therefore equal to the largest active
post's total. There is no slow continuous decay during this regime;
the moment a leader withdraws, sMax snaps down to the new leader.

Fallback decay applies only in the corner case where the tracker is
empty (every active post unwound). In that case, exponential decay
runs each epoch:

    for each epoch elapsed since sMaxLastUpdatedEpoch:
        sMax = (sMax * sMaxDecayRateRay) / RAY

Both `sMaxDecayRateRay` and the cap `sMaxDecayMaxEpochs` are
governance-configurable via setSMaxDecayRate and setSMaxDecayMaxEpochs.
Current defaults: rate = 9e17 (10% per epoch), cap = 30 epochs. The
cap prevents unbounded gas cost when catching up after a long idle
period.

After fallback decay, if any leader has reappeared in the tracker,
sMax is floored at that leader's total:

    sMax = max(decayed, leaderTotal)

Governance can also call rescanSMax(postIds) to rebuild the tracker
from an arbitrary list of candidate posts; this is useful if the
tracker has lost a leader to withdrawals and a backfill is needed.

A.8. Position Rescale

After each snapshot's epoch math (A.6) and side total recomputation,
the StakeEngine rescales all lots' weightedPosition values so that
the maximum position on each side is strictly less than sideTotal:

    if maxPosition >= sideTotal:
        target = sideTotal - 1
        for each lot:
            lot.weightedPosition = lot.weightedPosition * target / maxPosition

This prevents the edge case where earlier stakers withdraw and shrink
sideTotal below later stakers' positions, which would clamp those lots'
positionWeight to zero. The rescale preserves relative ordering of all
lots and applies to ghost lots (amount = 0) as well.

The rescale is a post-snapshot cleanup: during the current epoch's
computation, lots with oversized positions receive zero weight (via
the existing posShare > RAY clamp). The rescale fixes them for the
next epoch.

A PositionsRescaled event is emitted when rescale fires.

A.9. Mint and Burn

After all lots on both sides of a post are updated, the StakeEngine:

1. Sums total minted across all aligned lots.
2. Sums total burned across all misaligned lots.
3. Calls VSP_TOKEN.mint(address(this), totalMinted).
4. Calls VSP_TOKEN.burn(totalBurned).

The StakeEngine holds all staked tokens. Minting adds new tokens to
its balance; burning removes tokens from its balance. The net supply
change per epoch is (totalMinted - totalBurned).

A.10. View Projection

Read calls (getPostTotals, getUserStake) return projected values that
include unrealized gains and losses since the last snapshot. The
projection replicates the snapshot math without writing state,
including sMax decay projection. This ensures views are always current
without requiring gas.

Note: view projections do not project the position rescale (A.8).
Lots with oversized positions will show zero weight in projections
until the next snapshot materializes the rescale. This is consistent
with the write path, where those lots also receive zero weight during
the epoch that triggers the rescale.

A.11. Withdrawal

Users may withdraw any amount up to their lot's current amount.
Withdrawal reduces lot.amount and sideTotal, and then the StakeEngine
recomputes every lot's weightedPosition on the side using the midpoint
formula in A.2. As a result, partial withdrawal slightly shifts the
user (and every lot after them in the array) toward the front of the
queue — their relative array order is preserved, but their
weightedPosition shrinks because the side total they sit inside has
shrunk.

A fully-withdrawn user retains a ghost lot (amount = 0) at their
original array index. The lotIndex mapping still points there, so a
later top-up by the same user merges back into the same slot rather
than creating a new lot at the back of the queue. Ghost lots can be
removed by a governance call to compactLots(postId, side).

The lifo parameter on the withdraw function is accepted for ABI
compatibility but is ignored; lots are no longer FIFO/LIFO ranges,
just (user, side) pairs.

A.12. Governance Parameters

The following parameters are modifiable via governance (TimelockController):

- R_MIN_ANNUAL: minimum annual rate (StakeRatePolicy.setRates)
- R_MAX_ANNUAL: maximum annual rate (StakeRatePolicy.setRates)
- snapshotPeriod: minimum time between snapshots (StakeEngine.setSnapshotPeriod)
- sMaxDecayRateRay: fallback sMax decay rate (StakeEngine.setSMaxDecayRate); only consulted when no posts are active
- sMaxDecayMaxEpochs: cap on fallback-decay epochs per call (StakeEngine.setSMaxDecayMaxEpochs)
- maxIncomingEdges: ScoreEngine fan-in limit (ScoreEngine.setEdgeLimits)
- maxOutgoingLinks: ScoreEngine fan-out limit (ScoreEngine.setEdgeLimits)
- postingFeeVSP: posting fee in VSP (PostingFeePolicy.setPostingFee)
- minTotalStakeVSP: activity threshold (ClaimActivityPolicy.setMinTotalStake)

Current deployed values (Fuji testnet):
- R_MIN_ANNUAL = 0 (no minimum rate)
- R_MAX_ANNUAL = 1e18 (100% annual)
- snapshotPeriod = 1 day
- sMaxDecayRateRay = 9e17 (10% per epoch, fallback only)
- sMaxDecayMaxEpochs = 30
- maxIncomingEdges = 64 (sort by stake desc, ties: linkPostId asc; cut links contribute 0)
- maxOutgoingLinks = 64 (sort by stake desc, ties: linkPostId asc; cut links contribute 0)
- postingFeeVSP = 1e18 (1 VSP)
- minTotalStakeVSP = 1e18 (1 VSP)
- MAX_CLAIM_LENGTH = 2000 bytes (PostRegistry constant; not governance-configurable)
- MAX_DEPTH = 32 (ScoreEngine constant; not governance-configurable)

------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS_num = 0)

When VS_num is exactly zero, the snapshot short-circuits immediately.
No lots are modified; no tokens are minted or burned. Position rescale
still runs on the VS-neutral early-return path.

B.2. Incentive Against Post Fracturing

Because rBase depends on participationRay = T / sMax, posts with small
T relative to sMax have lower base rates. Staking into a shared
canonical post yields better returns than splitting across duplicates.

B.3. Lot Consolidation and Position

A user who stakes 100 VSP at position 0, then another 100 VSP when the
side total is 100, ends up with a single lot of 200 VSP at weighted
position (0*100 + 100*100) / 200 = 50. This is worse than a user who
staked 200 VSP at position 0 (weighted position 0), but better than a
user who staked 200 VSP at position 100.

B.4. sMax Tracking Tracks Current Activity

The top-3 leader tracker keeps sMax pinned to the largest active post's
total at all times. As soon as the previous leader withdraws or has
its stake burned below the second-place post's total, sMax snaps down
to the new leader. There is therefore no risk of a historical pump
permanently suppressing future participation factors: as soon as the
attacker exits, sMax follows them down. The fallback exponential
decay (A.7) is a safety net that only matters in the empty-protocol
corner case.

B.5. No Recursive Link Propagation in StakeEngine

Link influence on Verity Scores is computed by the ScoreEngine, not the
StakeEngine. The StakeEngine uses only direct stake totals (A, D) for
its rate computation. Effective VS (including link contributions) is a
read-only view provided by the ScoreEngine for display and analytics.

B.6. Single-Sided Positions

A user cannot hold stake on both sides of the same post. Attempting to
stake on the opposite side when the user already has a non-zero lot on
the current side reverts with OppositeSideStaked. To flip sides, the
user must withdraw fully from the current side first, then stake on the
new side.

B.7. Position Rescale Timing

The position rescale (A.8) is a post-snapshot cleanup. During the epoch
in which a withdrawal causes positions to exceed sideTotal, affected
lots receive zero weight — this is a one-epoch penalty. The rescale
runs after the epoch math and fixes positions for subsequent epochs.
Users can avoid the penalty by re-staking (which triggers a snapshot
and rescale) before the next natural snapshot fires.

B.8. Implementation Flexibility

The Solidity implementation may:
- Use epoch-based discrete updates with a configurable snapshot period.
- Apply rate updates lazily (on the next state-changing operation).
- Choose concrete governance parameter values via the TimelockController.
- Expose additional view functions for analytics.

As long as the semantics remain consistent with this appendix,
implementations are considered conformant.

------------------------------------------------------------------------------
Appendix C. Cycle Handling and Bounded Fan-In (Informative)
------------------------------------------------------------------------------

The ScoreEngine bounds both incoming-edge processing per claim
(maxIncomingEdges) and outgoing-link summation per parent
(maxOutgoingLinks). When a claim or parent has more edges than the
relevant cap, the edges are sorted by link stake descending — with
ties broken deterministically by linkPostId ascending — and only the
top-N participate.

For outgoing edges, this preserves conservation of influence: the
top-N outgoing links are exclusively the ones that sum into the
parent's denominator (sumOutgoingLinkStake) and exclusively the ones
that produce a non-zero numerator in the contribution formula. A
link outside the parent's top-N contributes zero. As a result, the
sum of linkShare values across all of a parent's outgoing links is
always ≤ 1.0, and link spam past the cap is fully self-defeating.

For incoming edges, the cap is just an information bound: edges
beyond the top-N are skipped, which loses information but does not
violate any invariant (incoming edges have no shared denominator
across them).

The deterministic tiebreak (linkPostId ascending = older link wins)
is essential so that off-chain indexers recomputing scores agree
with on-chain results when two links have identical stake.


The LinkGraph permits cycles (e.g., A challenges B, B challenges A).
The ScoreEngine's effectiveVSRay computation handles cycles as follows:

1. A stack of post IDs currently being computed is passed through
   recursive calls.
2. Before recursing into a parent, the engine checks if the parent's
   post ID is already on the stack.
3. If so, the parent's contribution for that path is 0 (not its base VS).
4. A hard depth limit of 32 truncates contributions to zero regardless.
5. The credibility gate (parent VS <= 0 => contribution 0) further
   stabilizes cycles by silencing claims whose VS drops to zero.

The result is that effectiveVS is well-defined and bounded on any
directed graph, not merely on a DAG.
