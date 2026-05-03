// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title IVeriSphereVSP
 * @notice Official Solidity interface for VeriSphere VSP Task 2.1
 * @dev This interface defines the core functions for the VeriSphere VSP protocol
 */
interface IVeriSphereVSP {
    // ---------- Events ----------

    /**
     * @notice Emitted when a new verification request is created
     * @param requestId Unique identifier for the verification request
     * @param requester Address of the entity requesting verification
     * @param dataHash Hash of the data to be verified
     * @param timestamp Block timestamp when request was created
     */
    event VerificationRequested(
        bytes32 indexed requestId,
        address indexed requester,
        bytes32 dataHash,
        uint256 timestamp
    );

    /**
     * @notice Emitted when a verification is completed
     * @param requestId Unique identifier for the verification request
     * @param verifier Address of the entity that performed verification
     * @param result True if verification passed, false otherwise
     * @param timestamp Block timestamp when verification was completed
     */
    event VerificationCompleted(
        bytes32 indexed requestId,
        address indexed verifier,
        bool result,
        uint256 timestamp
    );

    /**
     * @notice Emitted when a verifier is registered in the system
     * @param verifier Address of the registered verifier
     * @param metadataHash Hash pointing to verifier metadata
     * @param timestamp Block timestamp when registration occurred
     */
    event VerifierRegistered(
        address indexed verifier,
        bytes32 metadataHash,
        uint256 timestamp
    );

    /**
     * @notice Emitted when a verifier is removed from the system
     * @param verifier Address of the removed verifier
     * @param timestamp Block timestamp when removal occurred
     */
    event VerifierRemoved(
        address indexed verifier,
        uint256 timestamp
    );

    /**
     * @notice Emitted when the protocol fee is updated
     * @param oldFee Previous fee amount (in wei)
     * @param newFee New fee amount (in wei)
     * @param timestamp Block timestamp when fee was updated
     */
    event FeeUpdated(
        uint256 oldFee,
        uint256 newFee,
        uint256 timestamp
    );

    // ---------- Structs ----------

    /**
     * @notice Represents a verification request
     * @param requester Address that created the request
     * @param dataHash Hash of the data being verified
     * @param verifier Address assigned to verify (address(0) if unassigned)
     * @param completed Whether verification has been completed
     * @param result Result of verification (only valid if completed)
     * @param createdAt Timestamp when request was created
     * @param completedAt Timestamp when verification was completed (0 if not completed)
     */
    struct VerificationRequest {
        address requester;
        bytes32 dataHash;
        address verifier;
        bool completed;
        bool result;
        uint256 createdAt;
        uint256 completedAt;
    }

    /**
     * @notice Represents a registered verifier
     * @param active Whether the verifier is currently active
     * @param reputationScore Current reputation score (0-100)
     * @param totalVerifications Total number of verifications performed
     * @param successfulVerifications Number of successful verifications
     * @param metadataHash Hash pointing to verifier metadata
     * @param registeredAt Timestamp when verifier was registered
     */
    struct Verifier {
        bool active;
        uint8 reputationScore;
        uint256 totalVerifications;
        uint256 successfulVerifications;
        bytes32 metadataHash;
        uint256 registeredAt;
    }

    // ---------- State-Changing Functions ----------

    /**
     * @notice Creates a new verification request
     * @param dataHash Hash of the data to be verified
     * @return requestId Unique identifier for the created request
     * @dev Emits a VerificationRequested event
     *      Requires msg.value >= current fee
     */
    function requestVerification(bytes32 dataHash) external payable returns (bytes32 requestId);

    /**
     * @notice Assigns a verifier to a pending request
     * @param requestId Identifier of the verification request
     * @param verifier Address of the verifier to assign
     * @dev Only callable by the request owner or contract owner
     *      Request must not already be completed or assigned
     */
    function assignVerifier(bytes32 requestId, address verifier) external;

    /**
     * @notice Completes a verification with the result
     * @param requestId Identifier of the verification request
     * @param result True if verification passed, false otherwise
     * @dev Only callable by the assigned verifier
     *      Emits a VerificationCompleted event
     */
    function completeVerification(bytes32 requestId, bool result) external;

    /**
     * @notice Registers a new verifier in the system
     * @param metadataHash Hash pointing to verifier metadata (e.g., IPFS CID)
     * @dev Only callable by contract owner
     *      Emits a VerifierRegistered event
     */
    function registerVerifier(bytes32 metadataHash) external;

    /**
     * @notice Removes a verifier from the system
     * @param verifier Address of the verifier to remove
     * @dev Only callable by contract owner
     *      Emits a VerifierRemoved event
     */
    function removeVerifier(address verifier) external;

    /**
     * @notice Updates the protocol fee
     * @param newFee New fee amount in wei
     * @dev Only callable by contract owner
     *      Emits a FeeUpdated event
     */
    function updateFee(uint256 newFee) external;

    /**
     * @notice Withdraws accumulated fees to the contract owner
     * @dev Only callable by contract owner
     */
    function withdrawFees() external;

    // ---------- View Functions ----------

    /**
     * @notice Returns details of a verification request
     * @param requestId Identifier of the verification request
     * @return VerificationRequest struct with request details
     */
    function getRequest(bytes32 requestId) external view returns (VerificationRequest memory);

    /**
     * @notice Returns details of a registered verifier
     * @param verifier Address of the verifier
     * @return Verifier struct with verifier details
     */
    function getVerifier(address verifier) external view returns (Verifier memory);

    /**
     * @notice Returns the current protocol fee
     * @return Current fee amount in wei
     */
    function getFee() external view returns (uint256);

    /**
     * @notice Returns the contract owner address
     * @return Owner address
     */
    function owner() external view returns (address);

    /**
     * @notice Checks if an address is an active verifier
     * @param verifier Address to check
     * @return True if the address is an active verifier
     */
    function isActiveVerifier(address verifier) external view returns (bool);

    /**
     * @notice Returns the total number of verification requests
     * @return Total request count
     */
    function totalRequests() external view returns (uint256);

    /**
     * @notice Returns the total number of registered verifiers
     * @return Total verifier count
     */
    function totalVerifiers() external view returns (uint256);
}
