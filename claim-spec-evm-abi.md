# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.6 (MVP, ASCII only, link-aware)

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
    //                Max length: 500 bytes.
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
    // Stake VSP on a post, on either support or challenge side.
    // Reverts OppositeSideStaked if user already has stake on the other side.
    function stake(uint256 postId, uint8 side, uint256 amount) external;

    // Withdraw stake from a post. Reduces the user's consolidated lot.
    // lifo parameter is accepted for ABI compatibility but ignored.
    function withdraw(uint256 postId, uint8 side, uint256 amount, bool lifo) external;

    // Apply epoch growth/decay. Anyone may call; typically a keeper or backend.
    function updatePost(uint256 postId) external;

    // Returns projected totals (includes unrealized gains/losses).
    function getPostTotals(uint256 postId)
        external view returns (uint256 support, uint256 challenge);

    // Returns projected user stake (includes unrealized gains/losses).
    function getUserStake(address user, uint256 postId, uint8 side)
        external view returns (uint256);

    // Remove zero-amount ghost lots. Governance-only.
    function compactLots(uint256 postId, uint8 side) external;

    // Events
    event StakeAdded(uint256 indexed postId, address indexed staker, uint8 side, uint256 amount);
    event StakeWithdrawn(uint256 indexed postId, address indexed staker, uint8 side, uint256 amount, bool lifo);
    event PostUpdated(uint256 indexed postId, uint256 epoch, uint256 supportTotal, uint256 challengeTotal);
    event EpochMinted(uint256 indexed postId, uint256 amount);
    event EpochBurned(uint256 indexed postId, uint256 amount);
    event PositionsRescaled(uint256 indexed postId, uint8 side, uint256 oldMax, uint256 newCeiling);

    // Errors
    error InvalidSide();
    error AmountZero();
    error OppositeSideStaked();
    error NotEnoughStake();
    error ZeroAddressToken();
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
- Version: 0.6-mvp-links
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
a lot, the lot is merged:

    newPosition = (existing.weightedPosition * existing.amount
                   + queue.total * newAmount)
                  / (existing.amount + newAmount)

    existing.amount += newAmount

New lots enter at position = queue.total (back of the queue).
This means earlier, larger stakes have lower weightedPosition values.

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

A.6. Continuous Positional Weighting

Each lot's reward share is determined by its weightedPosition relative
to the side total. There are no discrete buckets or tranches; the
weight is a continuous linear function:

    positionWeight = 1 - (lot.weightedPosition / sideTotal)

A lot at position 0 (front of queue) has positionWeight = 1.0 (full
rate). A lot at position = sideTotal (hypothetical back) would have
positionWeight = 0.0 (no rate). In practice, positions are bounded
below sideTotal by the post-snapshot rescale (see A.8).

The epoch budget for each side is:

    budget = sideTotal * rBase / RAY

The budget is distributed proportionally to each lot's weighted stake:

    myWeightedStake = lot.amount * positionWeight
    totalWeightedStake = sum(myWeightedStake) across all lots on this side
    delta = budget * myWeightedStake / totalWeightedStake

If aligned (lot side matches VS sign):
    lot.amount += delta       (minted)
else:
    loss = min(delta, lot.amount)
    lot.amount -= loss        (burned)

Where "aligned" means:
- supportWins && lot.side == support, OR
- !supportWins && lot.side == challenge

Note: The `numTranches` storage variable and `setNumTranches` governance
function exist in the contract for ABI compatibility with earlier
versions. They are not consulted by the reward math.

A.7. sMax Decay

sMax decays over time to prevent stale historical peaks from
permanently suppressing participation factors on all future posts.

Decay rate: 0.5% per epoch (SMAX_DECAY_RATE_RAY = 995e15).

sMax is maintained via a top-3 post tracker. When a post's total
stake changes, the tracker is updated. If the leader's total is
below the current sMax, exponential decay is applied:

    for each epoch elapsed since sMaxLastUpdatedEpoch:
        sMax = (sMax * 995e15) / RAY

Decay is bounded: at most 3650 epochs (10 years) of decay are applied
in a single refresh, preventing unbounded gas cost if a post is
untouched for a long time.

After decay, sMax is floored at the current leader's total:

    sMax = max(decayed, leaderTotal)

If the leader's total exceeds the previous sMax, sMax is raised
immediately (no decay applied).

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
Withdrawal reduces lot.amount and sideTotal. The lot's
weightedPosition is NOT changed on withdrawal — the user retains
their positional advantage for the remaining stake.

A.12. Governance Parameters

The following parameters are modifiable via governance (TimelockController):

- R_MIN_ANNUAL: minimum annual rate (StakeRatePolicy.stakeIntRateMinRay)
- R_MAX_ANNUAL: maximum annual rate (StakeRatePolicy.stakeIntRateMaxRay)
- snapshotPeriod: minimum time between snapshots (StakeEngine.setSnapshotPeriod)
- maxIncomingEdges: ScoreEngine fan-in limit (ScoreEngine.setEdgeLimits)
- maxOutgoingLinks: ScoreEngine fan-out limit (ScoreEngine.setEdgeLimits)
- postingFeeVSP: posting fee in VSP (PostingFeePolicy.setPostingFee)
- minTotalStakeVSP: activity threshold (ClaimActivityPolicy.setMinTotalStake)
- numTranches: legacy field (StakeEngine.setNumTranches) — stored but not used

Current deployed values (Fuji testnet):
- R_MIN_ANNUAL = 0 (no minimum rate)
- R_MAX_ANNUAL = 1e18 (100% annual)
- snapshotPeriod = 1 day
- maxIncomingEdges = 64
- maxOutgoingLinks = 64
- postingFeeVSP = 1e18 (1 VSP)
- SMAX_DECAY_RATE_RAY = 995e15 (0.5% per epoch)

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

B.4. sMax Decay Prevents Historical Lock-In

Without decay, a single large historical post could set sMax to a value
that suppresses participation factors on all future posts indefinitely.
The 0.5% daily decay ensures sMax gradually tracks current activity.

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
Appendix C. Cycle Handling in ScoreEngine (Informative)
------------------------------------------------------------------------------

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
