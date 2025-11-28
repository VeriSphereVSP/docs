# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.3 (MVP Draft, ASCII only)

This document defines the ABI-level specification for the core VeriSphere
on-chain components:

- PostRegistry
- StakeEngine
- LinkGraph
- VSPToken (subset)
- Authority (subset)

The main body is pure ABI (interfaces, structs, events, errors).
All economic and behavioral explanations are in the appendices.

-------------------------------------------------------------------------------
1. Core Data Structures
-------------------------------------------------------------------------------

NOTE: These structs are conceptual. Actual storage layout and packing may vary.

----------------------------------------
1.1 Post
----------------------------------------

struct Post {
    uint256 postId;
    address creator;
    uint256 timestamp;
    string  text;
    uint256 supportTotal;
    uint256 challengeTotal;
}

----------------------------------------
1.2 StakeLot
----------------------------------------

struct StakeLot {
    address staker;
    uint256 amount;
    uint8   side;           // 0 = support, 1 = challenge
    uint32  positionIndex;  // queue index on chosen side
    uint256 entryTimestamp;
}

----------------------------------------
1.3 Relation
----------------------------------------

struct Relation {
    uint256 fromPost;
    uint256 toPost;
    uint8   relationType;   // 0 = support, 1 = challenge
    uint256 ctxStake;
}

-------------------------------------------------------------------------------
2. IPostRegistry ABI
-------------------------------------------------------------------------------

interface IPostRegistry {
    /// @notice Create a new immutable post (atomic claim).
    /// @param text The claim text, expected to be atomic and non-empty.
    /// @return postId The newly assigned post identifier.
    function createPost(string calldata text)
        external
        returns (uint256 postId);

    /// @notice Read a post by id.
    function getPost(uint256 postId)
        external
        view
        returns (
            address creator,
            uint256 timestamp,
            string memory text,
            uint256 supportTotal,
            uint256 challengeTotal
        );

    /// @notice Optional convenience view for base Verity Score.
    /// @dev Implementations may compute VS on-chain or off-chain.
    function getVerityScore(uint256 postId)
        external
        view
        returns (int256 vs);

    // Events

    event PostCreated(
        uint256 indexed postId,
        address indexed creator,
        string text
    );

    // Errors

    error EmptyText();
}

-------------------------------------------------------------------------------
3. IStakeEngine ABI
-------------------------------------------------------------------------------

interface IStakeEngine {
    /// @notice Stake VSP on a post, on either support or challenge side.
    /// @param postId The target post id.
    /// @param side   0 = support, 1 = challenge.
    /// @param amount Amount of VSP to stake (must be non-zero).
    function stake(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    /// @notice Withdraw some or all of a stake lot.
    /// @param postId   The target post id.
    /// @param lotIndex Index of the stake lot in that post-side queue.
    /// @param amount   Amount to withdraw from that lot (must be > 0 and <= lot amount).
    function withdraw(
        uint256 postId,
        uint256 lotIndex,
        uint256 amount
    ) external;

    /// @notice View all stake lots on a given side of a post.
    /// @dev Ordering reflects queue position (0 = earliest stake).
    function getStakeLots(uint256 postId, uint8 side)
        external
        view
        returns (StakeLot[] memory);

    /// @notice Optional view: total stake per side (for off-chain VS or analytics).
    function getTotals(uint256 postId)
        external
        view
        returns (uint256 supportTotal, uint256 challengeTotal);

    // Events

    event StakeAdded(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        uint32 positionIndex
    );

    event StakeWithdrawn(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        uint32 positionIndex
    );

    // Errors

    error InvalidSide();
    error AmountZero();
    error NotStaker();
    error InvalidLotIndex();
}

-------------------------------------------------------------------------------
4. ILinkGraph ABI
-------------------------------------------------------------------------------

interface ILinkGraph {
    /// @notice Create a contextual relation (edge) between two posts.
    /// @param fromPost      Child post used as evidence or counter-evidence.
    /// @param toPost        Parent post whose verity may be influenced.
    /// @param relationType  0 = support, 1 = challenge.
    /// @param ctxStake      VSP stake associated with this relation context.
    function linkPosts(
        uint256 fromPost,
        uint256 toPost,
        uint8 relationType,
        uint256 ctxStake
    ) external;

    /// @notice View relations where the given post is the parent (toPost).
    /// @dev Implementations may also expose per-fromPost views if needed.
    function getRelations(uint256 postId)
        external
        view
        returns (Relation[] memory);

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
}

-------------------------------------------------------------------------------
5. IVSPToken ABI (subset)
-------------------------------------------------------------------------------

interface IVSPToken {
    /// @notice Mint new VSP to an address.
    /// @dev Restricted to authorized minters in Authority.
    function mint(address to, uint256 amount) external;

    /// @notice Burn VSP from msg.sender.
    /// @dev Restricted to authorized burners in Authority.
    function burn(uint256 amount) external;

    /// @notice Burn VSP from another address with allowance.
    /// @dev Restricted to authorized burners in Authority.
    function burnFrom(address from, uint256 amount) external;

    // Standard ERC20 events

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Role errors (logical; implementation may use revert strings instead)

    error NotMinter();
    error NotBurner();
}

-------------------------------------------------------------------------------
6. IAuthority ABI (subset)
-------------------------------------------------------------------------------

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

-------------------------------------------------------------------------------
7. Versioning
-------------------------------------------------------------------------------

- Specification name: claim-spec-evm-abi
- Version: 0.3-mvp
- Chain target: Avalanche C-Chain / Subnet (EVM compatible)

Implementations should expose an on-chain constant or function that encodes
their spec version, for example:

    function specVersion() external pure returns (string memory);

Or a bytes32 constant representing a hash of this document.

-------------------------------------------------------------------------------
Appendix A. Economic Model (Informative)
-------------------------------------------------------------------------------

This appendix describes the intended economics for stake growth and loss.
It is not ABI, but semantic guidance for implementers and auditors.

A.1. Symbols

For a given post:

- A        = total support stake on the post
- D        = total challenge stake on the post
- T        = A + D  (total stake on the post)
- S        = total VSP supply
- VS       = base Verity Score in range [-100, +100]
- v        = abs(VS) / 100  (verity magnitude in [0,1])
- side     = 0 (support) or 1 (challenge) for a given StakeLot
- i        = 1-based queue position index on that side
- N_side   = total stake lots on that side
- R_min    = governance-controlled minimum annual rate
- R_max    = governance-controlled maximum annual rate
- alpha    = post size sensitivity exponent (> 0)
- P_min    = minimum post reward factor (0 < P_min <= 1)
- P_max    = maximum post reward factor (P_min <= P_max <= 1)
- dt       = time step length in years (for discrete update)
- n        = current amount staked in a given StakeLot
- n_next   = updated stake amount after one step
- r_eff    = effective annual rate for the post
- r_user   = effective annual rate for a specific StakeLot

A.2. Base Verity Score

Given A (support) and D (challenge), with T = A + D and T > 0:

    VS = (2 * (A / T) - 1) * 100

Clamp VS to [-100, +100].
If T is below the posting fee, implementations MAY treat VS as 0 for economics.

A.3. Post Reward Factor P (anti-fracturing)

Define x as the fraction of total supply staked on this post:

    x = T / S

Define the raw post factor:

    P_raw = x ^ alpha

Then clamp into a governance-defined band:

    P = clamp(P_raw, P_min, P_max)

Where clamp is:

    clamp(y, a, b) = min(max(y, a), b)

Intuition: larger, more consolidated posts (higher T relative to S)
produce a larger P (up to P_max), making it better to stake into one
shared post than to fracture into many tiny clones.

A.4. Effective Annual Rate r_eff

Given verity magnitude v and post factor P:

    r_eff = R_min + (R_max - R_min) * v * P

Properties:

- If VS = 0, then v = 0 and r_eff = R_min * P_min (or simply R_min, depending
  on how clamp is chosen). Implementations may choose to override this and
  treat VS = 0 as r_eff = 0 for economic neutrality.

- If abs(VS) = 100 and T is large relative to S, then v = 1 and P is near P_max,
  so r_eff tends toward R_max.

A.5. Positional Weighting w_i

Stake lots on each side (support/challenge) are ordered by arrival time.
Position 1 is the earliest, highest-risk lot on that side.

Define harmonic weights:

    H_N = sum_{j=1..N_side} (1 / j)

    w_i = (1 / i) / H_N

So:

- w_1 is largest
- w_i decreases with i
- sum of w_i over i from 1 to N_side is 1

A.6. Side Alignment and Sign sgn

Define sgn (the sign of the effective rate for a lot) as:

- If VS == 0:
    sgn = 0
- Else if side matches the sign of VS (support when VS > 0, challenge when VS < 0):
    sgn = +1
- Else:
    sgn = -1

A.7. Per-lot Annual Rate r_user

If VS == 0, we treat the position as neutral:

    r_user = 0

Else:

    r_user = sgn * r_eff * w_i

Where r_eff is from A.4 and w_i is from A.5.

A.8. Discrete Stake Update n_next

For a single time step dt (in years) for a given StakeLot with amount n:

- If VS == 0 or T is below the posting fee threshold:

      n_next = n

- Else:

      delta = n * r_user * dt
      n_next = max(0, n + delta)

Where r_user is from A.7.

Key behaviors:

- If sgn > 0 (aligned with VS), and VS is large in magnitude, and the post
  is large (P high), and the position is early (w_i high), then n_next can
  grow meaningfully over time.

- If sgn < 0 (opposed to VS) under the same conditions, n_next will shrink,
  potentially to zero (full economic loss).

- If a player moves from a large, old post into a tiny new post,
  they lose the high P associated with the large post and thus lose access
  to the best effective rates.

-------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
-------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS = 0)

When VS is exactly zero, the interpretation is "market unclear". The economic
model sets:

- r_user = 0
- n_next = n

for that period. This avoids punishing or rewarding either side when the
truth pressure is neutral.

B.2. Incentive Against Post Fracturing

Because the post reward factor P depends on T / S (total stake on the post
relative to total supply), small fractured posts have lower P values and thus
yield lower effective rates, even for early stakers.

Roughly:

- Everyone staking into one big canonical post will enjoy higher P and thus
  be closer to R_max (up to the harmonic and sign-based adjustments).

- The last staker on a large, high-P post will generally not be able to
  improve their situation by peeling off into a new tiny post, because the
  drop in P outweighs any positional advantage.

B.3. Incentive To Challenge Instead Of Clone

If a player disagrees with an existing claim, they can:

- Challenge the existing post (side = challenge), gaining access to the same
  post-level P (and thus potentially high rates if they are correct), or

- Create a new contradictory post with a very small T and thus small P,
  which is less attractive economically.

This structure encourages players to concentrate stake on a shared set of
canonical posts and use the challenge side rather than proliferating duplicate
or conflicting posts to farm "first position".

B.4. Implementation Flexibility

The actual Solidity implementation may:

- Apply rate updates on stake/withdraw operations, on a per-post update call,
  or via a keeper pattern.
- Approximate dt based on block timestamps and a chosen time granularity.
- Choose concrete values for R_min, R_max, alpha, P_min, P_max via governance.
- Expose additional view functions for analytics (for example, per-lot
  effective rate estimates).

As long as the semantics remain consistent with this appendix and the ABI in
the main body, implementations are considered conformant.
