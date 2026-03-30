# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.5 (MVP Draft, ASCII only, link-aware)

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

A Post is an atomic claim. Optionally it may act as a link from one claim to
another via targetPostId.

- targetPostId = 0      -> standalone claim
- targetPostId > 0      -> this post supports post targetPostId
- targetPostId < 0      -> this post challenges post abs(targetPostId)

Post-level support and challenge from direct stake are tracked separately from
link-based influence (which is handled by LinkGraph).

struct Post {
    address creator;
    uint256 timestamp;
    string  text;
    int256  targetPostId;    // 0 = standalone, >0 support link, <0 challenge link

    // Direct stake on this post (from StakeEngine)
    uint256 directSupportTotal;
    uint256 directChallengeTotal;
}

## 1.2 StakeLot

A StakeLot is a single, independent staking position in a post-side queue.
Multiple lots from the same staker are treated independently. Each lot has
a begin, end, and mid position within the side queue, used for queue-based
weighting.

struct StakeLot {
    address staker;
    uint256 amount;
    uint8   side;          // 0 = support, 1 = challenge
    uint256 begin;         // queue position start (from last toward first)
    uint256 end;           // queue position end
    uint256 mid;           // (begin + end) / 2
    uint256 entryEpoch;    // epoch index when lot was created
}

## 1.3 Relation

A Relation is an explicit link between two posts. It is created in the
LinkGraph and carries contextual stake (ctxStake). The economic impact of
links is modeled via LinkGraph summary functions, not by walking the full DAG
in StakeEngine.

struct Relation {
    uint256 fromPost;       // child / evidence post
    uint256 toPost;         // parent / target post
    uint8   relationType;   // 0 = support, 1 = challenge
    uint256 ctxStake;       // stake locked into this relation context
}

------------------------------------------------------------------------------
2. IPostRegistry ABI
------------------------------------------------------------------------------

interface IPostRegistry {
    // Create a new immutable post (atomic claim).
    // text           Claim text, expected to be atomic and non-empty.
    // targetPostId   0 for standalone; >0 supports that post; <0 challenges it.
    // Returns        Newly assigned postId.
    function createPost(string calldata text, int256 targetPostId)
        external
        returns (uint256 postId);

    // Read a post by id.
    function getPost(uint256 postId)
        external
        view
        returns (
            address creator,
            uint256 timestamp,
            string memory text,
            int256 targetPostId,
            uint256 directSupportTotal,
            uint256 directChallengeTotal
        );

    // Called by StakeEngine to sync direct stake totals for this post.
    function setDirectTotals(
        uint256 postId,
        uint256 supportTotal,
        uint256 challengeTotal
    ) external;

    // Convenience view for the base verity score using direct stake only.
    // This does not include link-based influence. Economic calculations
    // in StakeEngine will use effective totals that combine direct stake
    // with LinkGraph summaries (see Appendix A).
    function getBaseVerityScore(uint256 postId)
        external
        view
        returns (int256 vs);

    // Events

    event PostCreated(
        uint256 indexed postId,
        address indexed creator,
        int256 targetPostId,
        string text
    );

    event DirectTotalsUpdated(
        uint256 indexed postId,
        uint256 supportTotal,
        uint256 challengeTotal
    );

    // Errors

    error EmptyText();
    error InvalidTargetSelf();
    error NotStakeEngine();
}

------------------------------------------------------------------------------
3. IStakeEngine ABI
------------------------------------------------------------------------------

interface IStakeEngine {
    // Stake VSP on a post, on either support or challenge side.
    // postId   Target post id.
    // side     0 = support, 1 = challenge.
    // amount   Amount of VSP to stake (must be non-zero).
    function stake(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    // Withdraw stake from a post, choosing FIFO or LIFO across the caller's lots.
    // postId   Target post id.
    // side     0 = support, 1 = challenge.
    // amount   Total amount to withdraw.
    // lifo     If true, withdraw latest lots first; if false, earliest first.
    function withdraw(
        uint256 postId,
        uint8 side,
        uint256 amount,
        bool lifo
    ) external;

    // Apply daily epoch growth/decay to all lots for a post.
    // Any address may call; typically a keeper or backend.
    function updatePost(uint256 postId) external;

    // View total direct stake per side for a post.
    function getPostTotals(uint256 postId)
        external
        view
        returns (uint256 supportTotal, uint256 challengeTotal);

    // View lots on a given side for a post.
    function getLots(uint256 postId, uint8 side)
        external
        view
        returns (StakeLot[] memory);

    // Events

    event StakeAdded(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount
    );

    event StakeWithdrawn(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        bool lifo
    );

    event PostUpdated(
        uint256 indexed postId,
        uint256 epoch,
        uint256 supportTotal,
        uint256 challengeTotal
    );

    // Errors

    error InvalidSide();
    error AmountZero();
    error NotEnoughStake();
    error ZeroAddressToken();
}

------------------------------------------------------------------------------
4. ILinkGraph ABI
------------------------------------------------------------------------------

interface ILinkGraph {
    // Create a contextual relation (edge) between two posts.
    // fromPost      Child / evidence post id.
    // toPost        Parent / target post id.
    // relationType  0 = support, 1 = challenge.
    // ctxStake      VSP stake associated with this relation context.
    //
    // Must enforce:
    // - No cycles in the link graph (DAG only).
    // - fromPost != toPost.
    function linkPosts(
        uint256 fromPost,
        uint256 toPost,
        uint8 relationType,
        uint256 ctxStake
    ) external;

    // View relations where the given post is the parent (toPost).
    function getRelations(uint256 postId)
        external
        view
        returns (Relation[] memory);

    // Summary view for economic use:
    // Returns (linkSupportTotal, linkChallengeTotal) for the target post,
    // using the ctxStake of each relation and its relationType.
    function getLinkTotals(uint256 postId)
        external
        view
        returns (uint256 linkSupportTotal, uint256 linkChallengeTotal);

    // Events

    event RelationAdded(
        uint256 indexed fromPost,
        uint256 indexed toPost,
        uint8 relationType,
        uint256 ctxStake
    );

    // Errors

    error InvalidRelationType();
    error CycleDetected();
    error ZeroContextStake();
    error InvalidPostId();
}

------------------------------------------------------------------------------
5. IVSPToken ABI (subset)
------------------------------------------------------------------------------

interface IVSPToken {
    // Mint new VSP to an address.
    // Restricted to authorized minters in Authority.
    function mint(address to, uint256 amount) external;

    // Burn VSP from msg.sender.
    // Restricted to authorized burners in Authority.
    function burn(uint256 amount) external;

    // Burn VSP from another address with allowance.
    // Restricted to authorized burners in Authority.
    function burnFrom(address from, uint256 amount) external;

    // Standard ERC20-like functions
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);

    // Standard ERC20 events
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Role errors (logical; implementation may use revert strings instead)
    error NotMinter();
    error NotBurner();
}

------------------------------------------------------------------------------
6. IAuthority ABI (subset)
------------------------------------------------------------------------------

interface IAuthority {
    // Views
    function owner() external view returns (address);
    function isMinter(address who) external view returns (bool);
    function isBurner(address who) external view returns (bool);

    // Events
    event OwnerChanged(address indexed oldOwner, address indexed newOwner);
    event MinterSet(address indexed who, bool enabled);
    event BurnerSet(address indexed who, bool enabled);

    // Errors
    error NotOwner();
}

------------------------------------------------------------------------------
7. Versioning
------------------------------------------------------------------------------

- Specification name: claim-spec-evm-abi
- Version: 0.5-mvp-links
- Chain target: Avalanche C-Chain / Subnet (EVM compatible)

Implementations SHOULD expose an on-chain constant or function that encodes
their spec version, for example:

    function specVersion() external pure returns (string memory);

Or a bytes32 constant representing a hash of this document.

------------------------------------------------------------------------------
Appendix A. Economic Model (Normative, v2 — Tranche-Based)
------------------------------------------------------------------------------

This appendix is the NORMATIVE specification of stake economics.
It supersedes all previous descriptions of rate formulas, positional
weighting, and sMax behavior in other documents. The whitepaper and
architecture documents defer to this appendix on economic details.

This appendix matches the StakeEngine v2 Solidity implementation.

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
- numTranches (nT)  = governance-controlled positional tranche count (default 10)
- snapshotPeriod    = minimum time between O(N) snapshot updates (default 1 day)

Per StakeLot:

- amount             = current token amount (mutated by snapshots)
- weightedPosition   = stake-weighted queue position (see A.5)
- side               = 0 (support) or 1 (challenge)
- entryEpoch         = epoch when lot was first created

A.2. Lot Consolidation

There is exactly one StakeLot per user per side per post. When a user
stakes additional tokens on a side where they already have a lot, the
lot is merged:

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

A.6. Positional Tranche Weighting

Each lot is assigned to a tranche based on its weightedPosition
relative to the side total. Tranche 0 is the earliest (best);
tranche nT-1 is the latest (worst).

    tranche = (lot.weightedPosition * nT) / sideTotal
    if tranche >= nT: tranche = nT - 1

Position weight:

    positionWeight = ((nT - tranche) * RAY) / nT

This gives tranche 0 a weight of RAY (1.0) and tranche nT-1 a
weight of RAY/nT (e.g., 0.1 with 10 tranches).

Per-lot rate:

    rLot = (rBase * positionWeight) / RAY

Per-lot balance update:

    delta = (lot.amount * rLot) / RAY

    if aligned (lot side matches VS sign):
        lot.amount += delta       (minted)
    else:
        loss = min(delta, lot.amount)
        lot.amount -= loss        (burned)

Where "aligned" means:
- supportWins && lot.side == support, OR
- !supportWins && lot.side == challenge

A.7. sMax Decay

sMax is NOT monotonically increasing. It decays over time to prevent
stale historical peaks from permanently suppressing participation
factors on all future posts.

Decay is applied whenever sMax is refreshed (on any state-changing
operation):

    for each epoch elapsed since sMaxLastUpdatedEpoch:
        sMax = (sMax * 0.999e18) / RAY

Decay is bounded: at most 3650 epochs (10 years) of decay are applied
in a single refresh, preventing unbounded gas cost if a post is
untouched for a long time.

After decay, sMax is raised to at least the current post's total:

    if (sides[0].total + sides[1].total) > sMax:
        sMax = sides[0].total + sides[1].total

A.8. Mint and Burn

After all lots on both sides of a post are updated, the StakeEngine:

1. Sums total minted across all aligned lots.
2. Sums total burned across all misaligned lots.
3. Calls VSP_TOKEN.mint(address(this), totalMinted).
4. Calls VSP_TOKEN.burn(totalBurned).

The StakeEngine holds all staked tokens. Minting adds new tokens to
its balance; burning removes tokens from its balance. The net supply
change per epoch is (totalMinted - totalBurned).

A.9. View Projection

Read calls (getPostTotals, getUserStake) return projected values that
include unrealized gains and losses since the last snapshot. The
projection replicates the snapshot math without writing state,
including sMax decay projection. This ensures views are always current
without requiring gas.

A.10. Withdrawal

Users may withdraw any amount up to their lot's current amount.
Withdrawal reduces lot.amount and sideTotal. The lot's
weightedPosition is NOT changed on withdrawal — the user retains
their positional advantage for the remaining stake.

A.11. Governance Parameters

The following parameters are modifiable via governance (TimelockController):

- R_MIN_ANNUAL: minimum annual rate (StakeRatePolicy.stakeIntRateMinRay)
- R_MAX_ANNUAL: maximum annual rate (StakeRatePolicy.stakeIntRateMaxRay)
- numTranches: number of positional tranches (StakeEngine.setNumTranches)
- snapshotPeriod: minimum time between snapshots (StakeEngine.setSnapshotPeriod)
- postingFeeVSP: posting fee in VSP (PostingFeePolicy.setPostingFee)
- minTotalStakeVSP: activity threshold (ClaimActivityPolicy.setMinTotalStake)

Current deployed values (Fuji testnet):
- R_MIN_ANNUAL = 0 (no minimum rate)
- R_MAX_ANNUAL = 1e18 (100% annual)
- numTranches = 10
- snapshotPeriod = 1 day
- postingFeeVSP = 1e18 (1 VSP)

Note: The whitepaper historically referenced a 1% minimum rate.
This is not deployed. It may be set via governance in the future.

------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS_num = 0)

When VS_num is exactly zero, the snapshot short-circuits immediately.
No lots are modified; no tokens are minted or burned.

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
The 0.1% daily decay ensures sMax gradually tracks current activity.

B.5. No Recursive Link Propagation in StakeEngine

Link influence on Verity Scores is computed by the ScoreEngine, not the
StakeEngine. The StakeEngine uses only direct stake totals (A, D) for
its rate computation. Effective VS (including link contributions) is a
read-only view provided by the ScoreEngine for display and analytics.

B.6. Implementation Flexibility

The Solidity implementation may:
- Use epoch-based discrete updates with a configurable snapshot period.
- Apply rate updates lazily (on the next state-changing operation).
- Choose concrete governance parameter values via the TimelockController.
- Expose additional view functions for analytics.

As long as the semantics remain consistent with this appendix,
implementations are considered conformant.
