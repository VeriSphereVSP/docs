// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract GovernanceHub {
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 deadline;
        uint256 votesFor;
        uint256 votesAgainst;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted;
    uint256 public proposalCount;
    uint256 public quorum;
    address public executionAuthority;

    event ProposalCreated(uint256 indexed id, address indexed proposer, string description, uint256 deadline);
    event Voted(uint256 indexed proposalId, address indexed voter, bool support);
    event ProposalExecuted(uint256 indexed proposalId);

    modifier onlyExecutionAuthority() {
        require(msg.sender == executionAuthority, "Not execution authority");
        _;
    }

    constructor(uint256 _quorum, address _executionAuthority) {
        quorum = _quorum;
        executionAuthority = _executionAuthority;
    }

    function createProposal(string memory description, uint256 duration) external {
        require(bytes(description).length > 0, "Description cannot be empty");
        
        uint256 deadline = block.timestamp + duration;

        proposals[proposalCount] = Proposal({
            id: proposalCount,
            proposer: msg.sender,
            description: description,
            deadline: deadline,
            votesFor: 0,
            votesAgainst: 0,
            executed: false
        });

        emit ProposalCreated(proposalCount, msg.sender, description, deadline);
        proposalCount++;
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp < proposal.deadline, "Voting period has ended");
        require(!hasVoted[msg.sender][proposalId], "Already voted");

        if (support) {
            proposal.votesFor++;
        } else {
            proposal.votesAgainst++;
        }
        hasVoted[msg.sender][proposalId] = true;

        emit Voted(proposalId, msg.sender, support);
    }

    function executeProposal(uint256 proposalId) external onlyExecutionAuthority {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.deadline, "Proposal is still active");
        require(!proposal.executed, "Proposal already executed");
        require(proposal.votesFor + proposal.votesAgainst >= quorum, "Quorum not reached");

        proposal.executed = true;

        // Placeholder for execution logic
        // execute(proposal);

        emit ProposalExecuted(proposalId);
    }
}