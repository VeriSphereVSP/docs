# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.4 (MVP Draft, ASCII only)

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
```solidity
struct Post {
    uint256 postId;
    address creator;
    uint256 timestamp;
    string  text;
    uint256 supportTotal;
    uint256 challengeTotal;
}
```

----------------------------------------
1.2 StakeLot
----------------------------------------
```solidity
struct StakeLot {
    address staker;
    uint256 amount;
    uint8   side;           // 0 = support, 1 = challenge
    uint256 entryTimestamp; // unix timestamp of deposit
}
```

----------------------------------------
1.3 Relation
----------------------------------------
```solidity
struct Relation {
    uint256 fromPost;
    uint256 toPost;
    uint8   relationType;   // 0 = support, 1 = challenge
    uint256 ctxStake;
}
```

-------------------------------------------------------------------------------
2. IPostRegistry ABI
-------------------------------------------------------------------------------
```solidity
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
```

-------------------------------------------------------------------------------
3. IStakeEngine ABI
-------------------------------------------------------------------------------
```solidity
interface IStakeEngine {
    struct StakeLot {
        address staker;
        uint256 amount;
        uint8   side;           // 0 = support, 1 = challenge
        uint256 entryTimestamp; // unix timestamp of deposit
    }

    /// @notice Stake VSP on a post, on either support or challenge side.
    /// @param postId The target post id.
    /// @param side   0 = support, 1 = challenge.
    /// @param amount Amount of VSP to stake (must be non-zero).
    function stake(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    /// @notice Withdraw stake from a post using FIFO or LIFO selection.
    /// @dev This walks the caller's StakeLots on the chosen side, in FIFO or
    ///      LIFO order, until the requested amount is reached.
    /// @param postId   The target post id.
    /// @param side     0 = support, 1 = challenge.
    /// @param amount   Total amount to withdraw across lots.
    /// @param useLifo  If true, withdraw from latest lots first; otherwise
    ///                 withdraw from earliest lots first.
    function withdraw(
        uint256 postId,
        uint8 side,
        uint256 amount,
        bool useLifo
    ) external;

    /// @notice View all stake lots on a given side of a post.
    /// @dev Ordering reflects arrival time (index 0 = earliest stake).
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
        uint256 amount
    );

    event StakeWithdrawn(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount
    );

    // Errors

    error InvalidSide();
    error AmountZero();
    error NotStaker();
    error InsufficientStake();
}
```

-------------------------------------------------------------------------------
4. ILinkGraph ABI
-------------------------------------------------------------------------------
```solidity
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
```

-------------------------------------------------------------------------------
5. IVSPToken ABI (subset)
-------------------------------------------------------------------------------
```solidity
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
```

-------------------------------------------------------------------------------
6. IAuthority ABI (subset)
-------------------------------------------------------------------------------
```solidity
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
```

-------------------------------------------------------------------------------
7. Versioning
-------------------------------------------------------------------------------

- Specification name: claim-spec-evm-abi
- Version: 0.4-mvp
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
- S_total  = total VSP supply
- VS       = base Verity Score in range [-100, +100]
- v        = abs(VS) / 100  (verity magnitude in [0,1])
- side     = 0 (support) or 1 (challenge) for a given StakeLot
- R_min    = governance-controlled minimum annual rate
- R_max    = governance-controlled maximum annual rate
- n        = current amount staked in a given StakeLot
- n_next   = updated stake amount after one step
- r_eff    = effective annual rate for a post
- r_user   = effective annual rate for a specific StakeLot

Global, across posts:

- S_max    = maximum T across all active posts (largest staked post)
- m_i      = midpoint of queue segment occupied by StakeLot i
- m_max    = maximum midpoint across all StakeLots on all active posts

A.2. Base Verity Score

Given A (support) and D (challenge), with T = A + D and T > 0:

    VS = (2 * (A / T) - 1) * 100

Clamp VS to [-100, +100].
If T is below the posting fee, implementations MAY treat VS as 0 for economics.

A.3. Post Size Factor f_post

Define S_post as the total stake T on a post. Let S_max be the largest T
across all active posts in the system (posts with stake >= posting fee).

    f_post = S_post / S_max

Properties:

- 0 < f_post <= 1 for active posts
- The largest post has f_post = 1
- Smaller posts approach f_post near 0

This makes it economically preferable to concentrate stake into a canonical
post rather than fracturing into many small posts.

A.4. Queue Position Factor q_pos (Midpoint Based)

Each StakeLot occupies a contiguous segment of the queue on its side of a post.
Stake is ordered by arrival time on that side.

We define queue position from "back to front" as follows:

For a given side of a post, let cumulative stake start at 0 at the front
(newest) and grow toward the back (oldest). If we list StakeLots from newest
to oldest:

    lot 0: amount a0, occupies [0, a0]
    lot 1: amount a1, occupies [a0, a0 + a1]
    lot 2: amount a2, occupies [a0 + a1, a0 + a1 + a2]
    ...

In general, for StakeLot i in this newest-to-oldest ordering:

    low_i  = sum of a_j for j < i
    high_i = low_i + a_i

The midpoint of StakeLot i's queue segment is:

    m_i = (low_i + high_i) / 2

Now define m_max as the maximum midpoint across all StakeLots on all active
posts (on either side). Then the queue position factor for StakeLot i is:

    q_pos_i = m_i / m_max

Properties:

- 0 < q_pos_i <= 1
- StakeLots deeper in the queue (older stake) have larger midpoints and thus
  larger q_pos_i
- The deepest stake on the largest post tends toward q_pos_i = 1

A.5. Combined Effective Annual Rate r_eff

First define a post-level verity factor v:

    v = abs(VS) / 100

Then define the post-level effective annual rate:

    r_post = R_min + (R_max - R_min) * v * f_post

For a particular StakeLot i on that post, we apply queue position factor:

    r_eff_i = r_post * q_pos_i

A.6. Side Alignment and Sign sgn

Define sgn (the sign of the effective rate for a lot) as:

- If VS == 0:
    sgn = 0
- Else if side matches the sign of VS (support when VS > 0, challenge when VS < 0):
    sgn = +1
- Else:
    sgn = -1

A.7. Per-lot Annual Rate r_user

If VS == 0 or the post is below the economic activation threshold:

    r_user = 0

Else:

    r_user = sgn * r_eff_i

Where r_eff_i is from A.5 and sgn from A.6.

A.8. Epoch-based Stake Update n_next (1-day epochs, linear)

Let the epoch length be one day, and interpret annual rates linearly per day.
There are approximately 365 epochs per year.

For a single epoch for a given StakeLot with amount n:

- If VS == 0 or the post is below the economic activation threshold:

      n_next = n

- Else:

      daily_rate = r_user / 365
      delta      = n * daily_rate
      n_next     = max(0, n + delta)

This results in linear compounding across epochs: each day adjusts the stake
by a fraction of the annual rate, based on the current amount n.

Key behaviors:

- Early, deep stake on the largest posts (high f_post, high q_pos_i) gets
  rates near R_max when aligned with VS and loses near R_max when misaligned.
- Small, shallow posts or late-arriving stake get rates closer to R_min.
- Peeling off from a large post into a small new post usually hurts the
  effective rate, because f_post drops sharply even if queue position improves.

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

Because the post size factor f_post depends on S_post / S_max, small fractured
posts have lower f_post values and thus yield lower effective rates, even for
early stakers.

Roughly:

- Everyone staking into one big canonical post will enjoy higher f_post and
  thus be closer to R_max (up to the side alignment and queue position
  adjustments).
- The last staker on a large, high-f_post post will generally not be able to
  improve their situation by peeling off into a new tiny post, because the
  drop in f_post outweighs any positional advantage.

B.3. Incentive To Challenge Instead Of Clone

If a player disagrees with an existing claim, they can:

- Challenge the existing post (side = challenge), gaining access to the same
  post-level f_post (and thus potentially high rates if they are correct), or

- Create a new contradictory post with a very small S_post and thus small
  f_post, which is less attractive economically.

This structure encourages players to concentrate stake on a shared set of
canonical posts and use the challenge side rather than proliferating duplicate
or conflicting posts to farm "first position".

B.4. Implementation Flexibility

The actual Solidity implementation may:

- Apply rate updates on stake/withdraw operations, on a per-post update call,
  or via a keeper pattern.
- Approximate epoch timing based on block timestamps.
- Choose concrete values for R_min, R_max via governance.
- Expose additional view functions for analytics (for example, per-lot
  effective rate estimates, f_post, and q_pos_i).

As long as the semantics remain consistent with this appendix and the ABI in
the main body, implementations are considered conformant.
