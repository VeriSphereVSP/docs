// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

/**
 * @title VotingContract
 * @dev Implements voting process along with vote delegation
 */
contract VotingContract is ReentrancyGuard, Ownable {
    using SafeMath for uint256;

    struct Voter {
        bool voted;  // if true, that person already voted
        address delegate; // person delegated to
        uint vote;   // index of the voted proposal
    }

    struct Proposal {
        bytes32 name;   // short name (up to 32 bytes)
        uint voteCount; // number of accumulated votes
    }

    address public chairperson;

    mapping(address => Voter) public voters;

    Proposal[] public proposals;

    event VoteCasted(address indexed voter, uint proposalIndex);
    event VotingDelegated(address indexed from, address indexed to);
    event ProposalAdded(bytes32 proposalName);
    event ChairpersonChanged(address indexed newChairperson);

    modifier onlyChairperson() {
        require(msg.sender == chairperson, "Caller is not the chairperson");
        _;
    }

    constructor(bytes32[] memory proposalNames) {
        chairperson = msg.sender;
        voters[chairperson].voted = false;

        for (uint i = 0; i < proposalNames.length; i++) {
            proposals.push(Proposal({
                name: proposalNames[i],
                voteCount: 0
            }));
            emit ProposalAdded(proposalNames[i]);
        }
    }

    /**
     * @dev Give your vote (including votes delegated to you) to proposal `proposals[proposal].name`.
     * @param proposal index of proposal in the proposals array
     */
    function vote(uint proposal) external nonReentrant {
        Voter storage sender = voters[msg.sender];
        require(!sender.voted, "Already voted.");
        require(proposal < proposals.length, "Invalid proposal index.");

        sender.voted = true;
        sender.vote = proposal;

        proposals[proposal].voteCount += 1;
        emit VoteCasted(msg.sender, proposal);
    }

    /**
     * @dev Delegate your vote to the voter `to`.
     * @param to address to which vote is delegated
     */
    function delegate(address to) external nonReentrant {
        Voter storage sender = voters[msg.sender];
        require(!sender.voted, "You already voted.");
        require(to != msg.sender, "Self-delegation is disallowed.");

        while (voters[to].delegate != address(0)) {
            to = voters[to].delegate;

            // We found a loop in the delegation, not allowed.
            require(to != msg.sender, "Found loop in delegation.");
        }

        sender.voted = true;
        sender.delegate = to;
        Voter storage delegate_ = voters[to];
        if (delegate_.voted) {
            proposals[delegate_.vote].voteCount += 1;
        }
        emit VotingDelegated(msg.sender, to);
    }

    /**
     * @dev Computes the winning proposal taking all previous votes into account.
     * @return winningProposal_ index of winning proposal in the proposals array
     */
    function winningProposal() public view returns (uint winningProposal_) {
        uint winningVoteCount = 0;
        for (uint p = 0; p < proposals.length; p++) {
            if (proposals[p].voteCount > winningVoteCount) {
                winningVoteCount = proposals[p].voteCount;
                winningProposal_ = p;
            }
        }
    }

    /**
     * @dev Gets the name of the winning proposal
     * @return winnerName_ name of the winning proposal
     */
    function winnerName() external view returns (bytes32 winnerName_) {
        winnerName_ = proposals[winningProposal()].name;
    }

    /**
     * @dev Changes the chairperson of the voting contract
     * @param newChairperson address of the new chairperson
     */
    function changeChairperson(address newChairperson) external onlyOwner {
        require(newChairperson != address(0), "Zero address not allowed.");
        chairperson = newChairperson;
        emit ChairpersonChanged(newChairperson);
    }

    /**
     * @dev Adds a new proposal to the list of proposals
     * @param proposalName name of the new proposal
     */
    function addProposal(bytes32 proposalName) external onlyChairperson {
        proposals.push(Proposal({
            name: proposalName,
            voteCount: 0
        }));
        emit ProposalAdded(proposalName);
    }
}
