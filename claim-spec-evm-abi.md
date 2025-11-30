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
```
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
```
struct StakeLot {
    address staker;
    uint256 amount;
    uint8   side;           // 0 = support, 1 = challenge
    uint32  positionIndex;  // queue index on chosen side
    uint256 entryTimestamp;
}
```
----------------------------------------
1.3 Relation
----------------------------------------
```
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
- Version: 0.3-mvp
- Chain target: Avalanche C-Chain / Subnet (EVM compatible)

Implementations should expose an on-chain constant or function that encodes
their spec version, for example:

    function specVersion() external pure returns (string memory);

Or a bytes32 constant representing a hash of this document.

# VeriSphere Claim Specification – Appendices (Epoch-Based, Linear)

Version: 0.4 (MVP)  
ASCII only

These appendices replace Appendix A and Appendix B in claim_spec_evm_abi.md,
incorporating:

- Epoch length = 1 day
- Linear compounding per epoch
- Final definitions for f_post and f_pos

-------------------------------------------------------------------------------
Appendix A. Economic Model (Informative)
-------------------------------------------------------------------------------

A.1. Epoch Structure
--------------------

VeriSphere uses **discrete 1‑day epochs** for stake updates.

Let:

- EPOCH_SECONDS = 86_400
- YEAR_SECONDS = 31_536_000
- dt = EPOCH_SECONDS / YEAR_SECONDS = 1/365

At the **start of each epoch**, the following values are snapshotted:

- Per post:
  - A = support total
  - D = challenge total
  - T = A + D
  - VS = Verity Score
  - f_post
- Global:
  - S_max = max(T across all active posts)
  - N_max = max(queue length in stake units across posts)
- Per lot:
  - stake-span endpoints for positional factor

Stake created during an epoch begins earning in the **next epoch**.

A.2. Base Verity Score (VS)
---------------------------

Given:

- A = support total
- D = challenge total
- T = A + D

If T > 0:

    VS = (2 * (A / T) - 1) * 100

Clamp VS into [-100, +100].

Define:

    v = abs(VS) / 100

A.3. Post Size Factor f_post
----------------------------

Let:

- T = total stake on post
- S_max = largest T on any active post

Then:

    f_post = T / S_max

A.4. Positional Factor f_pos
-----------------------------

Queue positions are measured **from the tail**.

Example:

    Total stake = 4.1

    A stakes 1.5 → [4.1, 2.6]
    B stakes 1.5 → [2.6, 1.1]
    C stakes 1.1 → [1.1, 0.0]

For a lot span:

    [x_end, x_start]

Compute:

    pos_i = (x_end + x_start) / 2

Normalize:

    f_pos = pos_i / N_max

Clamp to [0,1].

A.5. Effective Annual Rate r_eff
--------------------------------

Given R_min, R_max, v, f_post:

    r_eff = R_min + (R_max - R_min) * v * f_post

A.6. Side Alignment sgn
-----------------------

If VS == 0:

    sgn = 0

Else if (support AND VS > 0) or (challenge AND VS < 0):

    sgn = +1

Else:

    sgn = -1

A.7. Per-Lot Annual Rate r_user
-------------------------------

If VS == 0:

    r_user = 0

Else:

    r_user = sgn * r_eff * f_pos

A.8. Epoch Update (Linear)
--------------------------

Let n = current stake amount.

If VS == 0:

    n_next = n

Else:

    delta = n * r_user * dt
    n_next = max(0, n + delta)

-------------------------------------------------------------------------------
Appendix B. Behavioral Notes (Informative)
-------------------------------------------------------------------------------

B.1. Neutral VS
---------------

VS = 0 → no one gains or loses.

B.2. Anti-Fracturing
---------------------

f_post = T / S_max ensures:

- Large shared posts → high f_post → high r_eff.
- Small fractured posts → low f_post → poor economics.

B.3. Challenge Instead of Clone
-------------------------------

A challenger on a large post inherits its high f_post rather than starting
a new tiny post with low f_post.

B.4. Queue Incentives
---------------------

Early stakers on large queues get top f_pos.
Late stakers get smaller f_pos.

B.5. Implementation Flexibility
-------------------------------

Solidity implementations may:

- Update on stake/withdraw operations,
- Use per-post tick functions,
- Cache snapshot values per epoch,
- Adjust R_min, R_max, epoch length, etc. via governance.

-------------------------------------------------------------------------------
