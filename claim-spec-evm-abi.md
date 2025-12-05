# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)
Version: 0.52 (MVP Draft, ASCII only)

This document defines the ABI-level specification for the core VeriSphere
on-chain components:

- PostRegistry
- StakeEngine
- LinkGraph
- VSPToken (subset)
- Authority (subset)

The main body is pure ABI (interfaces, structs, events, errors).
All economic and behavioral explanations are in the appendices.

----
## 1. Core Data Structures

NOTE: These structs are conceptual. Actual storage layout and packing may vary.


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

----
## 1.2 StakeLot
----------------------------------------

Each explicit user stake is represented as an independent lot. Multiple stakes
from the same address are separate StakeLots and are not merged.

```solidity
struct StakeLot {
    address staker;
    uint256 amount;        // current principal in this lot
    uint8   side;          // 0 = support, 1 = challenge

    // Queue position in stake-units (measured from the queue tail).
    // These are updated when lots are created or partially withdrawn.
    uint256 beginStake;    // inclusive
    uint256 endStake;      // exclusive

    uint256 entryTimestamp;
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

    /// @notice Optional view: total stake per side.
    function getTotals(uint256 postId)
        external
        view
        returns (uint256 supportTotal, uint256 challengeTotal);

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
    /// @notice Stake VSP on a post, on either support or challenge side.
    /// @param postId The target post id.
    /// @param side   0 = support, 1 = challenge.
    /// @param amount Amount of VSP to stake (must be non-zero).
    function stake(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    /// @notice Withdraw stake lots FIFO (from earliest stake to latest).
    /// @param postId The target post id.
    /// @param side   0 = support, 1 = challenge.
    /// @param amount Amount to withdraw (must be > 0).
    function withdrawFIFO(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    /// @notice Withdraw stake lots LIFO (from latest stake to earliest).
    /// @param postId The target post id.
    /// @param side   0 = support, 1 = challenge.
    /// @param amount Amount to withdraw (must be > 0).
    function withdrawLIFO(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    /// @notice View all stake lots on a given side of a post.
    /// @dev Ordering reflects queue position in stake-units
    ///      (beginStake ascending).
    function getStakeLots(uint256 postId, uint8 side)
        external
        view
        returns (StakeLot[] memory);

    /// @notice Optional view: total stake per side (for off-chain VS or analytics).
    function getTotals(uint256 postId)
        external
        view
        returns (uint256 supportTotal, uint256 challengeTotal);

    /// @notice Optional: current epoch index (for analytics).
    function currentEpoch()
        external
        view
        returns (uint256 epochIndex);

    // Events

    event StakeAdded(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        uint256 beginStake,
        uint256 endStake
    );

    event StakeWithdrawn(
        uint256 indexed postId,
        address indexed staker,
        uint8 side,
        uint256 amount,
        bool   fifo
    );

    event EpochApplied(
        uint256 indexed epochIndex,
        uint256 timestamp
    );

    // Errors

    error InvalidSide();
    error AmountZero();
    error NotStaker();
    error InsufficientStake();
}
```

Notes:

- The StakeEngine is responsible for calling into VSPToken (transferFrom / transfer)
  for stake in and stake out.
- Epoch application (accrual and burn) may be triggered lazily (per post) or via
  an external keeper; the exact function surface is implementation-specific and
  not mandated by this ABI.

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
    /// @notice Standard ERC20 interface plus mint/burn.
    function totalSupply() external view returns (uint256);

    function balanceOf(address account)
        external
        view
        returns (uint256);

    function transfer(address to, uint256 amount)
        external
        returns (bool);

    function allowance(address owner, address spender)
        external
        view
        returns (uint256);

    function approve(address spender, uint256 amount)
        external
        returns (bool);

    function transferFrom(address from, address to, uint256 amount)
        external
        returns (bool);

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

    // Management

    function setOwner(address newOwner) external;
    function setMinter(address who, bool enabled) external;
    function setBurner(address who, bool enabled) external;

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
- Version: 0.52-mvp
- Chain target: Avalanche C-Chain / Subnet (EVM compatible)

Implementations SHOULD expose an on-chain constant or function that encodes
their spec version, for example:

```solidity
function specVersion() external pure returns (string memory);
```

Or a bytes32 constant representing a hash of this document.

-------------------------------------------------------------------------------
Appendix A. Economic Model (Informative)
-------------------------------------------------------------------------------

This appendix describes the intended economics for stake growth and loss.
It is not ABI, but semantic guidance for implementers and auditors.

A.1. Symbols
------------

For a given post i:

- A_i         = total support stake on the post
- D_i         = total challenge stake on the post
- T_i         = A_i + D_i  (total stake on the post)
- VS_i        = base Verity Score in range [-100, +100]
- v_i         = abs(VS_i) / 100 (verity magnitude in [0,1])
- S_total     = total VSP supply

Global:

- S_max       = max T_i over all active posts (largest post by stake)
- Q_len(p,s)  = total stake-units in queue for post p, side s
- Q_max       = max Q_len(p,s) over all posts and sides (global largest queue)

Per StakeLot j on post p, side s:

- amount_j      = current principal in lot j
- side_j        = 0 (support) or 1 (challenge)
- beginStake_j  = lot's begin position in stake-units from queue tail
- endStake_j    = lot's end position in stake-units from queue tail
- midStake_j    = (beginStake_j + endStake_j) / 2
- epochIndex    = global epoch index (monotonically increasing)

Governance parameters:

- R_min_annual  = minimum annual rate (per year)
- R_max_annual  = maximum annual rate (per year)
- P_post_min    = minimum post factor (0 < P_post_min <= 1)
- P_post_max    = maximum post factor (P_post_min <= P_post_max <= 1)
- P_pos_min     = minimum position factor (0 < P_pos_min <= 1)
- P_pos_max     = maximum position factor (P_pos_min <= P_pos_max <= 1)
- alpha_post    = exponent for post-size function (> 0)
- alpha_pos     = exponent for position function (> 0)
- epochsPerYear = number of epochs per year (e.g. 365 for daily)

A.2. Base Verity Score
----------------------

Given A_i (support) and D_i (challenge) for post i, with T_i = A_i + D_i and T_i > 0:

    VS_i = (2 * (A_i / T_i) - 1) * 100

Clamp VS_i to [-100, +100].

If T_i is below the posting fee threshold, implementations MAY treat VS_i as 0
for economic purposes.

A.3. Global Normalization (S_max and Q_max)
-------------------------------------------

Define:

    S_max = max T_i across all posts with T_i > 0

If there are no active posts (no stake), S_max is treated as 1 for normalization
to avoid division by zero.

Define:

    Q_len(p,s) = sum of lot.amount across all lots in the queue for (post p, side s)

    Q_max = max Q_len(p,s) across all posts and sides with Q_len > 0

If there are no queues with stake, Q_max is treated as 1 for normalization.

These global maxima are used to ensure that:

- Stake on the largest posts gets access to the highest economic band.
- Stake on very small posts does not get artificially high rates.
- Moving stake from a large post to a tiny new post generally reduces reward.

A.4. Post Size Factor f_post
----------------------------

For post i:

    if S_max == 0:
        f_post_raw = 0
    else:
        f_post_raw = T_i / S_max

Then clamp into a governance-defined band and optionally apply an exponent:

    f_post = clamp(f_post_raw, P_post_min, P_post_max)
    f_post = f_post ** alpha_post

where clamp(y, a, b) = min(max(y, a), b).

Intuition:

- If T_i is equal to the largest post stake, f_post_raw = 1.
- If T_i is small compared to the largest post, f_post_raw is small.
- Clamping prevents extremely tiny posts from going to zero and extremely
  large posts from exceeding 1.
- alpha_post > 1 makes the function more "top-heavy"; alpha_post < 1 makes
  it more forgiving to smaller posts.

A.5. Positional Factor f_pos (Queue Midpoint)
---------------------------------------------

Each stake lot has a beginStake and endStake that partition the queue in
stake-units. Queues are considered from the tail (earliest stake) at 0 up to
the head (latest stake) at Q_len(p,s).

For a given lot j on queue (p,s):

    midStake_j = (beginStake_j + endStake_j) / 2

Define a raw global-normalized position factor:

    if Q_max == 0:
        f_pos_raw = 0
    else:
        f_pos_raw = 1.0 - (midStake_j / Q_max)

Interpretation:

- When a lot is very early in a very large queue (midStake_j small, Q_max large),
  f_pos_raw is near 1.
- When a lot is very late in the largest queue (midStake_j near Q_max),
  f_pos_raw is near 0.
- Lots on smaller queues are normalized by the global Q_max, so their f_pos_raw
  generally cannot exceed the early positions on larger queues.

Then clamp and exponentiate:

    f_pos = clamp(f_pos_raw, P_pos_min, P_pos_max)
    f_pos = f_pos ** alpha_pos

This yields a position factor in (0,1], where:

- Early lots on large queues get high f_pos.
- Late lots and lots on small queues get lower f_pos.

A.6. Verity Alignment and Sign
------------------------------

For post i:

- If VS_i == 0, the market is neutral and there should be no reward or burn
  for that epoch.

Define a sign for each lot j on post i:

- If VS_i == 0:
      sgn_j = 0
- Else if side_j == 0 (support) and VS_i > 0:
      sgn_j = +1
- Else if side_j == 1 (challenge) and VS_i < 0:
      sgn_j = +1
- Else:
      sgn_j = -1

So:

- sgn_j = +1 means the lot is currently aligned with the Verity Score.
- sgn_j = -1 means the lot is currently opposed.
- sgn_j = 0 means neutral (no economic effect that epoch).

A.7. Effective Annual Rate per Lot
----------------------------------

Let v_i = abs(VS_i) / 100 (verity magnitude), so v_i is in [0,1].

Compute the post-level annual rate band:

    r_band = R_min_annual + (R_max_annual - R_min_annual) * v_i

This interpolates between R_min_annual and R_max_annual based on how
strong the Verity Score is in magnitude.

Then apply post size and position factors:

    r_mag = r_band * f_post * f_pos

Finally, incorporate alignment:

    r_annual_j = sgn_j * r_mag

Properties:

- If VS_i == 0, then v_i = 0 and sgn_j = 0, so r_annual_j = 0.
- If VS_i is large and the post is large and the position is early,
  r_annual_j has large magnitude (positive or negative).
- If the post is tiny or the lot is late, r_annual_j is closer to zero.

A.8. Epoch-Based Compounding (Non-linear)
-----------------------------------------

Time is discretized into epochs of fixed length (for example, 1 day). Let:

    epochsPerYear = 365  (for daily epochs)
    r_annual_j     = annual rate for lot j (from A.7)

Define the per-epoch rate using continuous compounding:

    r_epoch_j = exp(r_annual_j / epochsPerYear) - 1

For small r_annual_j, this is approximately r_annual_j / epochsPerYear, but the
exponential form gives a consistent non-linear compounding behavior across
different magnitudes of r_annual_j.

Given a lot with current amount amount_j at the start of an epoch:

- If VS_i == 0 or T_i is below the posting fee threshold:

      amount_next_j = amount_j

- Else:

      amount_next_j = amount_j * (1 + r_epoch_j)

and the implementation MUST clamp:

      if amount_next_j < 0:
          amount_next_j = 0

In practice, implementers can cap the minimum to zero and optionally impose a
maximum growth per epoch to avoid extreme jumps under edge parameters.

A.9. Epoch Length and dt
------------------------

With daily epochs and continuous compounding, dt (in years) is:

    dt = 1.0 / epochsPerYear

and:

    r_epoch_j = exp(r_annual_j * dt) - 1

Implementations MAY approximate the exponential for gas efficiency, for example:

- Use a Taylor expansion for small |r_annual_j * dt|.
- Precompute lookup tables for reasonable ranges of r_annual_j.
- Fall back to linear approximation:

      r_epoch_j approx r_annual_j * dt

as long as the direction (sign) and qualitative behavior are preserved.

A.10. Summary of Per-Epoch Update
---------------------------------

For each epoch:

1. For each post i:
    - Compute A_i, D_i, T_i.
    - Compute VS_i.
    - Track S_max and Q_max across all posts and sides.

2. For each StakeLot j on post i:
    - Compute f_post from T_i and S_max.
    - Compute midStake_j and f_pos from midStake_j and Q_max.
    - Compute v_i = abs(VS_i)/100 and sgn_j based on VS_i and side_j.
    - Compute r_annual_j.
    - Compute r_epoch_j.
    - Update amount_j to amount_next_j.

Stake movement (stake, withdrawFIFO, withdrawLIFO) should:

- Apply any pending epoch updates for that post and side before modifying
  queues and amounts.
- Update beginStake and endStake for affected lots.

-------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
-------------------------------------------------------------------------------

B.1. Neutral Verity Score (VS = 0)
----------------------------------

When VS_i is exactly zero, the interpretation is "market unclear". The economic
model sets:

- sgn_j = 0
- r_annual_j = 0
- r_epoch_j = 0
- amount_next_j = amount_j

for that epoch. This avoids punishing or rewarding either side when the
truth pressure is neutral.

B.2. Incentive Against Post Fracturing
--------------------------------------

Because the post factor f_post is based on T_i relative to S_max, and the
position factor f_pos is based on midStake_j relative to Q_max, a staker
who peels off from a large, canonical post into a small new post generally:

- Loses f_post (the new post is much smaller than S_max).
- Cannot gain enough f_pos advantage to offset the drop in f_post,
  because Q_max is global and dominated by the largest queues.

As a result, early participation in large canonical posts is generally
economically superior to creating many small duplicate posts.

B.3. Incentive To Challenge Instead Of Clone
--------------------------------------------

If a player disagrees with an existing claim, they can:

- Challenge the existing post (side = challenge), gaining access to the same
  post-level f_post as supporters, but with opposite alignment sign, or

- Create a new contradictory post with a very small T_i and thus small f_post.

Because the new post starts tiny, both supporters and challengers on that post
see reduced economic intensity compared to staking into the existing large post.
This encourages concentrated debate around canonical claims rather than a
proliferation of near-duplicate posts.

B.4. FIFO vs LIFO Withdraw
--------------------------

Each call to stake creates a new StakeLot, even if the same address has
staked before. Users may later choose:

- withdrawFIFO: redeem earliest lots first (preserving later positions).
- withdrawLIFO: redeem latest lots first (preserving early, high-leverage
  positions).

This allows users to manage their risk and accounting needs without
changing the economics of queue ordering for other participants.

B.5. Implementation Flexibility
-------------------------------

The actual Solidity implementation may:

- Apply epoch updates lazily per post or via a global keeper.
- Approximate exp() for r_epoch_j in a gas-efficient way.
- Tune R_min_annual, R_max_annual, alpha_post, alpha_pos, P_post_min,
  P_post_max, P_pos_min, P_pos_max, and epochsPerYear via governance.
- Expose additional view functions for analytics (for example, per-lot
  estimated epoch rate).

As long as the semantics remain consistent with this appendix and the ABI in
the main body, implementations are considered conformant.
