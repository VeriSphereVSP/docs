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
Appendix A. Economic Model (Informative, Link-Aware)
------------------------------------------------------------------------------

This appendix describes the intended economics for stake growth and loss.
It is not ABI, but semantic guidance for implementers and auditors.

A.1. Symbols

For a given post P:

- A        = direct support stake on P (from StakeEngine)
- D        = direct challenge stake on P (from StakeEngine)
- Lp       = support stake from incoming links (LinkGraph)
- Lm       = challenge stake from incoming links (LinkGraph)
- A_eff    = effective support = A + Lp
- D_eff    = effective challenge = D + Lm
- T_eff    = A_eff + D_eff  (total effective stake)
- S_total  = total VSP supply
- VS       = base Verity Score in range [-100, +100]
- v        = abs(VS) / 100  (verity magnitude in [0,1])
- side     = 0 (support) or 1 (challenge) for a given StakeLot
- R_min    = governance-controlled minimum annual rate
- R_max    = governance-controlled maximum annual rate
- P_min    = minimum post reward factor (0 < P_min <= 1)
- P_max    = maximum post reward factor (P_min <= P_max <= 1)
- dt       = time step length in years (epoch length / 365)
- n        = current amount staked in a given StakeLot
- r_eff    = effective annual rate for the post
- r_user   = effective annual rate for a specific StakeLot
- sMax     = global maximum total stake across all posts (monotonic)
- mid      = midpoint of the StakeLot in the side queue, from last toward first

A.2. Base Verity Score (effective, link-aware)

For a post P, using effective totals that include links:

    A_eff = A + Lp
    D_eff = D + Lm
    T_eff = A_eff + D_eff

If T_eff == 0, VS is defined as 0 (no information).

Otherwise:

    VS = (2 * (A_eff / T_eff) - 1) * 100

Clamp VS to [-100, +100].

Note: The base verity score stored or exposed by PostRegistry may consider only
direct stake (A, D). The economic engine in StakeEngine MUST use A_eff and D_eff,
combining direct stake with LinkGraph totals, when computing VS for growth/decay.

A.3. Link Contributions

Each relation in LinkGraph has:

- relationType = 0 (support) or 1 (challenge)
- ctxStake     = stake committed to that relation

For a given target post P:

    Lp = sum of ctxStake over all relations with relationType = support and toPost = P
    Lm = sum of ctxStake over all relations with relationType = challenge and toPost = P

The LinkGraph implementation SHOULD maintain these aggregates incrementally so
that getLinkTotals(postId) is O(1). There is no recursive propagation; each link
affects only its direct target, which keeps gas usage bounded.

A.4. Post Reward Factor (size-based, anti-fracturing)

Define x as the fraction of total supply staked on this post:

    x = T_eff / S_total

We treat x as a fixed-point value in [0, 1]. For MVP, take a simple linear
post factor and clamp it between P_min and P_max:

    P_raw = x
    P = clamp(P_raw, P_min, P_max)

Where clamp(y, a, b) = min(max(y, a), b).

Intuition: Larger, more consolidated posts (higher T_eff relative to S_total)
have higher P and thus earn rates nearer R_max, making it better to stake into
shared canonical posts than to fracture stake into many tiny clones.

A.5. Effective Annual Rate r_eff

Given verity magnitude v and post factor P:

    r_eff = R_min + (R_max - R_min) * v * P

Properties:

- If VS = 0, then v = 0 and r_eff collapses toward R_min (or 0, depending
  on implementation). MVP may treat VS = 0 as r_eff = 0 for neutrality.
- If abs(VS) = 100 and T_eff is large relative to S_total, then v = 1 and
  P is near P_max, so r_eff tends toward R_max.

A.6. Positional Weighting via mid and sMax

Stake lots on each side are ordered by arrival time. The queue is laid out
from last to first as a continuous axis, and each lot has a midpoint:

- mid is between begin and end (see StakeLot definition)
- sMax is the global maximum total stake observed across all posts

Define the positional weight for a lot as:

    w = mid / sMax

in fixed-point [0,1], clamped if needed. This means:

- The earliest, largest stakes on the biggest posts have mid near sMax and
  get w near 1.
- Late, small stakes on small posts have w near 0.

A.7. Side Alignment and Sign

Define sign alignment as:

- If VS == 0: sign = 0 (neutral)
- Else if side matches the sign of VS (support when VS > 0, challenge when VS < 0):
    sign = +1
- Else:
    sign = -1

A.8. Per-lot Annual Rate r_user

If VS == 0 or T_eff is below the posting fee threshold, the lot is neutral:

    r_user = 0

Else:

    r_user = sign * r_eff * w

Where r_eff is from A.5 and w is from A.6.

A.9. Discrete Stake Update n_next

We use epoch-based discrete updates. Let one epoch be EPOCH_LENGTH seconds,
and let dt = EPOCH_LENGTH / (365 days) in years. For a given StakeLot with
amount n:

- If VS == 0 or T_eff below threshold:

      n_next = n

- Else:

      delta = n * r_user * dt
      n_next = max(0, n + delta)

Key behaviors:

- If sign > 0 (aligned with VS), and VS is high, and T_eff is large, and
  mid is high relative to sMax, then the lot grows meaningfully over time.
- If sign < 0 (opposed to VS) under the same conditions, the lot shrinks,
  potentially to zero (total economic loss).
- Moving from a large, old post into a tiny new post loses the advantage of
  high P and high sMax-weighted position, reducing achievable returns.

------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS = 0)

When VS is exactly zero, the market is "unclear". The economic model treats
lots as neutral for that epoch:

- r_user = 0
- n_next = n

No one wins or loses while VS is neutral.

B.2. Incentive Against Post Fracturing

Because the post reward factor P depends on T_eff / S_total, small fractured
posts have lower P values and yield lower effective rates, even for early
stakers. It is generally better economically to stake into shared canonical
posts than to create many near-duplicate posts with low T_eff.

B.3. Incentive To Link Instead Of Clone

If a player wants to support or challenge an existing claim, they have two
main options:

- Stake directly on the post (support or challenge), or
- Create a link post plus a LinkGraph relation with ctxStake.

Because link-based ctxStake contributes to the effective totals of the target
post via Lp and Lm, there is real economic gain to building a coherent web of
evidence instead of proliferating contradictory or duplicate standalone posts.

B.4. No Recursive Propagation On-Chain

Link influence is local: each relation affects only its direct target via
ctxStake. There is no on-chain recursion over the DAG. This keeps gas usage
bounded and prevents denial-of-service via long or adversarial chains of links.

Global, recursive truth propagation (for example, multi-hop confidence scores
or PageRank-style measures) is left to the off-chain application layer, which
can re-derive the full DAG and expose richer scores without gas limits.

B.5. Implementation Flexibility

The actual Solidity implementation may:

- Apply rate updates on stake/withdraw operations, on a per-post update call,
  or via a keeper pattern.
- Approximate dt based on block timestamps and a chosen time granularity.
- Choose concrete values for R_min, R_max, P_min, P_max via governance.
- Expose additional view functions for analytics (for example, per-lot
  effective rate estimates or per-post effective A_eff and D_eff).

As long as the semantics remain consistent with this appendix and the ABI in
the main body, implementations are considered conformant.
