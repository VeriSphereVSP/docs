// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title IVeriSphereClaim
 * @dev Interface for the VeriSphere Claim Specification
 * Based on Task 2.1 of the MVP roadmap
 */
interface IVeriSphereClaim {
    struct ClaimData {
        address claimant;
        uint256 amount;
        bytes32 proof;
        uint256 expiration;
    }

    event ClaimSubmitted(bytes32 indexed claimId, address indexed claimant, uint256 amount);
    event ClaimVerified(bytes32 indexed claimId, address indexed verifier);

    function submitClaim(ClaimData calldata data) external returns (bytes32 claimId);
    function verifyClaim(bytes32 claimId, bytes calldata signature) external returns (bool);
    function getClaimStatus(bytes32 claimId) external view returns (uint8 status);
}
