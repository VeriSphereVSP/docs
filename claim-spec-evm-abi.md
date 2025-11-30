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
Implementations MAY use different internal representations as long as they can
reproduce the same semantics at the ABI boundary.

----------------------------------------
1.1 Post
----------------------------------------
```
struct Post {
    uint256 postId;
    address creator;
    uint256 timestamp;
    string  text;
    uint256 supportTotal;    // total stake on support side
    uint256 challengeTotal;  // total stake on challenge side
}
```

----------------------------------------
1.2 StakeSegment
----------------------------------------
A StakeSegment represents a contiguous range on a side-specific stake axis
for a given post. The axis is denominated in VSP units and ordered from
"latest stake" at 0 up to "earliest stake" at totalSideStake.

```
struct StakeSegment {
    address staker;
    uint8   side;        // 0 = support, 1 = challenge
    uint256 amount;      // VSP amount represented by this segment
    uint256 start;       // inclusive, in stake units, 0 = most recent
    uint256 end;         // exclusive, in stake units, end > start
    uint256 timestamp;   // last movement affecting this segment
}
```

Semantics:

- For a given (postId, side), all segments form a partition of
  [0, totalSideStake] with no gaps and no overlaps.
- New stake is appended at the "tail" of the queue:
    - New segment is [0, amount]
    - Existing segments have their [start, end] shifted upward by +amount
- Earliest stake (highest risk) sits at the highest coordinates on the axis.

Implementations MAY choose more gas-efficient internal representations (e.g.,
per-staker aggregates, prefix sums) but MUST preserve the logical meaning of
segment positions and midpoints as described in Appendix A.

----------------------------------------
1.3 Relation
----------------------------------------
```
struct Relation {
    uint256 fromPost;
    uint256 toPost;
    uint8   relationType;   // 0 = support, 1 = challenge
    uint256 ctxStake;       // contextual stake associated with this edge
}
```

-------------------------------------------------------------------------------
2. IPostRegistry ABI
-------------------------------------------------------------------------------
```
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
    ///      If unimplemented, callers should derive VS externally.
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
```
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

    /// @notice Withdraw some or all stake from a given segment.
    /// @param postId        The target post id.
    /// @param side          0 = support, 1 = challenge.
    /// @param segmentIndex  Index of the segment in that post-side queue.
    /// @param amount        Amount to withdraw from that segment (must be > 0 and <= segment amount).
    function withdraw(
        uint256 postId,
        uint8 side,
        uint256 segmentIndex,
        uint256 amount
    ) external;

    /// @notice View all stake segments on a given side of a post.
    /// @dev Ordering reflects queue position by axis coordinate:
    ///      segments[0] has the lowest [start, end],
    ///      segments[segments.length - 1] has the highest.
    function getStakeSegments(uint256 postId, uint8 side)
        external
        view
        returns (StakeSegment[] memory);

    /// @notice Optional view: total stake per side (for off-chain VS or analytics).
    function getTotals(uint256 postId)
        external
        view
        returns (uint256 supportTotal, uint256 challengeTotal);

    /// @notice Optional view: total stake length for a given side of a post.
    function getSideTotal(uint256 postId, uint8 side)
        external
        view
        returns (uint256 sideTotal);

    // Events

    event StakeAdded(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        uint256 start,
        uint256 end
    );

    event StakeWithdrawn(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        uint256 start,
        uint256 end
    );

    // Errors

    error InvalidSide();
    error AmountZero();
    error NotStaker();
    error InvalidSegmentIndex();
    error WithdrawTooLarge();
}
```

-------------------------------------------------------------------------------
4. ILinkGraph ABI
-------------------------------------------------------------------------------
```
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
```
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

    /// @notice Transfer tokens to another address.
    function transfer(address to, uint256 amount) external returns (bool);

    /// @notice Transfer tokens from one address to another, subject to allowance.
    function transferFrom(address from, address to, uint256 amount) external returns (bool);

    /// @notice Approve another address to spend tokens on behalf of msg.sender.
    function approve(address spender, uint256 amount) external returns (bool);

    function balanceOf(address account) external view returns (uint256);
    function allowance(address owner, address spender) external view returns (uint256);

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
```
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

For a given post and a given epoch (default: 1 day):

- A         = total support stake on the post
- D         = total challenge stake on the post
- T_post    = A + D  (total stake on the post)
- T_max     = maximum T_post across all active posts (T_max > 0)
- VS        = base Verity Score in range [-100, +100]
- v         = abs(VS) / 100  (verity magnitude in [0,1])
- side      = 0 (support) or 1 (challenge) for a given StakeSegment
- sgn       = alignment sign (+1, 0, -1; see A.5)
- R_min     = governance-controlled minimum annual rate (per year)
- R_max     = governance-controlled maximum annual rate (per year)
- f_post    = post size factor in [0,1]
- f_pos     = positional factor in [0,1] for a segment on a side queue
- r_eff     = effective annual rate at the post level
- r_user    = effective annual rate for a specific segment
- r_epoch   = effective per-epoch rate for a specific segment
- dt_year   = epoch length in years (for 1 day: 1/365)
- n         = current amount staked in a given StakeSegment at epoch start
- n_next    = updated stake amount after one epoch

Unless otherwise changed by governance, the default epoch length is 1 day
and compounding is linear per epoch (simple interest per step).

A.2. Base Verity Score

Given A (support) and D (challenge), with T_post = A + D and T_post > 0:

    VS = (2 * (A / T_post) - 1) * 100

Clamp VS to [-100, +100].

If T_post is below the posting fee threshold, implementations MAY treat VS
as 0 for economics (no gain or loss until the post has "enough" skin in the game).

A.3. Post Size Factor f_post (anti-fracturing)

Let T_post be the total stake on this post and T_max be the maximum total
stake among all active posts (T_max > 0). Define:

    f_post = T_post / T_max

Properties:

- 0 < f_post <= 1 for any active post with non-zero stake.
- The largest post (by total stake) has f_post = 1.
- Smaller posts have f_post less than 1.

Intuition: concentrating stake into a shared canonical post is economically
superior to fragmenting that stake across many tiny posts.

A.4. Side Queue and Positional Factor f_pos

For each post and each side (support or challenge), we define a stake axis
in units of VSP:

- The axis runs from 0 (most recent stake) up to L_side (total stake on that side).
- Each StakeSegment covers [start, end] with 0 <= start < end <= L_side.
- Segments partition [0, L_side] with no gaps or overlaps.

When a new stake of amount "a" is added to that side:

- The new segment for the caller is logically [0, a].
- All existing segments are shifted upward by +a on both start and end.
- Thus, earlier stakes occupy larger coordinate values and are considered
  "ahead in the queue".

Let:
- L_side = total stake on that side of the post (support or challenge).
- N_max  = maximum L_side across all posts and sides (L_side > 0, N_max > 0).

For a segment with coordinates [start, end], define its midpoint:

    m = (start + end) / 2

Then define the positional factor:

    f_pos = m / N_max

Properties:

- Segments closer to the "front" (earliest stakes) have higher m and thus higher f_pos.
- Segments closer to the "back" (most recent stakes) have lower m and thus lower f_pos.
- On the largest queues (L_side near N_max), early segments can achieve f_pos near 1.

This ensures that:

- Earliest stakes on the largest, most important posts get the strongest
  reward or penalty (largest magnitude effect).
- Late or small-post stakes sit closer to f_pos near 0.

A.5. Alignment Sign sgn

Define sgn, the sign of the effective rate for a segment, as:

- If VS == 0:
      sgn = 0
- Else if side matches the sign of VS:
      (support when VS > 0, challenge when VS < 0)
      sgn = +1
- Else:
      sgn = -1

This captures:

- Aligned with truth pressure -> positive sign (potential growth).
- Opposed to truth pressure -> negative sign (potential decay).
- Neutral truth pressure (VS = 0) -> no change.

A.6. Effective Annual Rate r_eff

Combine verity magnitude v, post factor f_post and the global rate band:

    v = abs(VS) / 100       // in [0,1]
    r_eff = R_min + (R_max - R_min) * v * f_post

Notes:

- If VS = 0, then v = 0 and r_eff = R_min.
  However, we will neutralize VS = 0 at the segment level (see A.8),
  so no net gain or loss occurs in that case.
- If abs(VS) is large and the post is large (f_post near 1), then r_eff
  can approach R_max in magnitude for aligned segments, and -R_max for
  misaligned segments after applying sgn and f_pos.

A.7. Per-segment Annual Rate r_user

Given r_eff, f_pos, and sgn:

    r_user = sgn * r_eff * f_pos

Interpretation:

- Aligned early stakes on large posts (sgn = +1, f_pos near 1, f_post near 1)
  experience rates near +R_max.
- Misaligned early stakes on large posts (sgn = -1, f_pos near 1, f_post near 1)
  experience rates near -R_max (rapid burn).
- Late stakes (small f_pos) and small posts (small f_post) see muted effects.

A.8. Epoch Rate and Discrete Stake Update n_next

The protocol uses discrete epochs of length 1 day and linear compounding.
Let:

    dt_year = 1 / 365       // epoch length in years (approximate)

First, derive the per-epoch rate r_epoch from the annual r_user:

    r_epoch = r_user * dt_year

Then, for a segment with amount n at the start of the epoch, the updated
amount n_next at the end of the epoch is:

- If VS == 0 or T_post is below the posting fee threshold:

      n_next = n

- Else:

      n_next = max(0, n * (1 + r_epoch))

Key behaviors:

- If sgn > 0 (aligned) and the post is large and early in the queue,
  n grows over time, approaching an annualized return near R_max.
- If sgn < 0 (misaligned) under the same conditions, n shrinks, potentially
  to zero (full loss).
- If VS = 0, no side gains or loses stake during that epoch.
- If a staker peels off from a large canonical post into a tiny post,
  f_post drops sharply, so r_user and thus r_epoch drop, preventing them
  from gaming "first position" on trivial posts.

-------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
-------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS = 0)

When VS is exactly zero, the interpretation is "market unclear".
The economic model sets:

    r_user  = 0
    r_epoch = 0
    n_next  = n

for that epoch. This avoids punishing or rewarding either side when the
truth pressure is neutral.

B.2. Incentive Against Post Fracturing

Because the post factor f_post is T_post / T_max, small fractured posts have
lower f_post and thus lower effective rates, even if a staker manages to
obtain an early position on those posts.

Roughly:

- Everyone staking into one big canonical post will enjoy higher f_post and
  thus be closer to the top of the R_min to R_max band (subject to VS and
  f_pos).
- The last staker on a large, high-f_post post will generally not be able
  to improve their situation by peeling off into a new tiny post, because
  the drop in f_post outweighs any positional advantage at f_pos.

B.3. Incentive To Challenge Instead Of Clone

If a player disagrees with an existing claim, they can:

- Challenge the existing post (side = challenge), gaining access to the same
  f_post (and thus potentially high magnitude rates if they are correct), or

- Create a new contradictory post with a very small T_post and thus small
  f_post, which is less attractive economically.

This structure encourages players to concentrate stake on a shared set of
canonical posts and use the challenge side rather than proliferating
duplicate or conflicting posts to farm "first position".

B.4. Epoch Mechanics

The implementation is free to choose how to apply epoch-based updates, for example:

- Apply updates lazily whenever a stake or withdrawal occurs, using the
  difference in timestamps to estimate how many epochs have passed.
- Use a keeper or cron-like mechanism to periodically call an update
  function on busy posts.
- Batch updates for gas efficiency.

All such mechanisms should be consistent with the linear per-epoch update
described above and use R_min, R_max, and dt_year as parameterized by
governance.

B.5. Implementation Flexibility

The actual Solidity implementation may:

- Approximate dt_year more precisely (e.g., 1 / 365.25).
- Choose concrete values for R_min and R_max via governance.
- Store segments in a compressed or aggregated way (for example, one segment
  per staker per side per post) as long as the queue semantics and midpoint-
  based interpretation are preserved.
- Expose additional view functions for analytics (for example, per-segment
  effective rate estimates).

As long as the semantics remain consistent with this appendix and the ABI in
the main body, implementations are considered conformant.
