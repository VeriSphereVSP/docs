# VeriSphere Claim and Staking Specification (EVM-ABI Formal Style)

---

## Overview
This document defines the formal ABI-level specification for the VeriSphere on-chain components:
- PostRegistry
- StakeEngine
- LinkGraph
- VSPToken (subset)
- Authority (subset)

All content uses ASCII only.

---

# 1. Core Data Structures

## 1.1 Post

struct Post {
    uint256 postId;
    address creator;
    uint256 timestamp;
    string text;
    uint256 supportTotal;
    uint256 challengeTotal;
}

---

## 1.2 StakeLot

struct StakeLot {
    address staker;
    uint256 amount;
    uint8 side;            // 0 = support, 1 = challenge
    uint32 positionIndex;
    uint256 entryTimestamp;
}

---

## 1.3 Relation

struct Relation {
    uint256 fromPost;
    uint256 toPost;
    uint8 relationType; // 0 = support, 1 = challenge
    uint256 ctxStake;
}

---
  
# 2. IPostRegistry ABI

interface IPostRegistry {

    function createPost(string calldata text)
        external
        returns (uint256 postId);

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

    event PostCreated(
        uint256 indexed postId,
        address indexed creator,
        string text
    );

    error EmptyText();
}

---

# 3. IStakeEngine ABI

interface IStakeEngine {

    function stake(
        uint256 postId,
        uint8 side,
        uint256 amount
    ) external;

    function withdraw(
        uint256 postId,
        uint256 lotIndex,
        uint256 amount
    ) external;

    function getStakeLots(uint256 postId, uint8 side)
        external
        view
        returns (StakeLot[] memory);

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

    error InvalidSide();
    error AmountZero();
    error NotStaker();
}

---

# 4. ILinkGraph ABI

interface ILinkGraph {

    function linkPosts(
        uint256 fromPost,
        uint256 toPost,
        uint8 relationType,
        uint256 ctxStake
    ) external;

    function getRelations(uint256 postId)
        external
        view
        returns (Relation[] memory);

    event RelationAdded(
        uint256 indexed fromPost,
        uint256 indexed toPost,
        uint8 relationType,
        uint256 ctxStake
    );

    error InvalidRelationType();
    error CycleDetected();
}

---

# 5. IVSPToken ABI (subset)

interface IVSPToken {
    function mint(address to, uint256 amount) external;
    function burn(address from, uint256 amount) external;
}

event Transfer(address indexed from, address indexed to, uint256 value);

error NotMinter();
error NotBurner();

---

# 6. IAuthority ABI (subset)

interface IAuthority {

    function owner() external view returns (address);

    function isMinter(address who) external view returns (bool);

    function isBurner(address who) external view returns (bool);

    event OwnerChanged(address indexed oldOwner, address indexed newOwner);
    event MinterSet(address indexed who, bool enabled);
    event BurnerSet(address indexed who, bool enabled);

    error NotOwner();
}

---

