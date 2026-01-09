const { expect } = require("chai");
const { ethers } = require("hardhat");
const { time } = require("@nomicfoundation/hardhat-network-helpers");

describe("GovernanceHub", function () {
  let governanceHub;
  let owner;
  let executionAuthority;
  let voter1;
  let voter2;
  let voter3;

  const QUORUM = 3;
  const VOTING_DURATION = 86400; // 1 day in seconds

  beforeEach(async function () {
    [owner, executionAuthority, voter1, voter2, voter3] = await ethers.getSigners();

    const GovernanceHub = await ethers.getContractFactory("GovernanceHub");
    governanceHub = await GovernanceHub.deploy(QUORUM, executionAuthority.address);
    await governanceHub.deployed();
  });

  describe("Deployment", function () {
    it("should set the correct quorum", async function () {
      expect(await governanceHub.quorum()).to.equal(QUORUM);
    });

    it("should set the correct execution authority", async function () {
      expect(await governanceHub.executionAuthority()).to.equal(executionAuthority.address);
    });

    it("should start with zero proposals", async function () {
      expect(await governanceHub.proposalCount()).to.equal(0);
    });
  });

  describe("createProposal", function () {
    it("should create a proposal with correct parameters", async function () {
      const description = "Upgrade protocol to v2";

      await expect(governanceHub.connect(voter1).createProposal(description, VOTING_DURATION))
        .to.emit(governanceHub, "ProposalCreated")
        .withArgs(0, voter1.address, description, await getDeadline(VOTING_DURATION));

      const proposal = await governanceHub.proposals(0);
      expect(proposal.proposer).to.equal(voter1.address);
      expect(proposal.description).to.equal(description);
      expect(proposal.votesFor).to.equal(0);
      expect(proposal.votesAgainst).to.equal(0);
      expect(proposal.executed).to.equal(false);
    });

    it("should increment proposal count", async function () {
      await governanceHub.createProposal("Proposal 1", VOTING_DURATION);
      await governanceHub.createProposal("Proposal 2", VOTING_DURATION);

      expect(await governanceHub.proposalCount()).to.equal(2);
    });

    it("should reject empty description", async function () {
      await expect(governanceHub.createProposal("", VOTING_DURATION))
        .to.be.revertedWith("Description cannot be empty");
    });
  });

  describe("vote", function () {
    beforeEach(async function () {
      await governanceHub.createProposal("Test proposal", VOTING_DURATION);
    });

    it("should allow voting for a proposal", async function () {
      await expect(governanceHub.connect(voter1).vote(0, true))
        .to.emit(governanceHub, "Voted")
        .withArgs(0, voter1.address, true);

      const proposal = await governanceHub.proposals(0);
      expect(proposal.votesFor).to.equal(1);
      expect(proposal.votesAgainst).to.equal(0);
    });

    it("should allow voting against a proposal", async function () {
      await governanceHub.connect(voter1).vote(0, false);

      const proposal = await governanceHub.proposals(0);
      expect(proposal.votesFor).to.equal(0);
      expect(proposal.votesAgainst).to.equal(1);
    });

    it("should prevent double voting", async function () {
      await governanceHub.connect(voter1).vote(0, true);

      await expect(governanceHub.connect(voter1).vote(0, false))
        .to.be.revertedWith("Already voted");
    });

    it("should reject votes after deadline", async function () {
      await time.increase(VOTING_DURATION + 1);

      await expect(governanceHub.connect(voter1).vote(0, true))
        .to.be.revertedWith("Voting period has ended");
    });

    it("should track multiple voters correctly", async function () {
      await governanceHub.connect(voter1).vote(0, true);
      await governanceHub.connect(voter2).vote(0, true);
      await governanceHub.connect(voter3).vote(0, false);

      const proposal = await governanceHub.proposals(0);
      expect(proposal.votesFor).to.equal(2);
      expect(proposal.votesAgainst).to.equal(1);
    });
  });

  describe("executeProposal", function () {
    beforeEach(async function () {
      await governanceHub.createProposal("Test proposal", VOTING_DURATION);
      await governanceHub.connect(voter1).vote(0, true);
      await governanceHub.connect(voter2).vote(0, true);
      await governanceHub.connect(voter3).vote(0, true);
    });

    it("should execute proposal after deadline with quorum met", async function () {
      await time.increase(VOTING_DURATION + 1);

      await expect(governanceHub.connect(executionAuthority).executeProposal(0))
        .to.emit(governanceHub, "ProposalExecuted")
        .withArgs(0);

      const proposal = await governanceHub.proposals(0);
      expect(proposal.executed).to.equal(true);
    });

    it("should reject execution before deadline", async function () {
      await expect(governanceHub.connect(executionAuthority).executeProposal(0))
        .to.be.revertedWith("Proposal is still active");
    });

    it("should reject execution without quorum", async function () {
      await governanceHub.createProposal("Low vote proposal", VOTING_DURATION);
      await governanceHub.connect(voter1).vote(1, true);

      await time.increase(VOTING_DURATION + 1);

      await expect(governanceHub.connect(executionAuthority).executeProposal(1))
        .to.be.revertedWith("Quorum not reached");
    });

    it("should reject double execution", async function () {
      await time.increase(VOTING_DURATION + 1);
      await governanceHub.connect(executionAuthority).executeProposal(0);

      await expect(governanceHub.connect(executionAuthority).executeProposal(0))
        .to.be.revertedWith("Proposal already executed");
    });

    it("should reject execution by non-authority", async function () {
      await time.increase(VOTING_DURATION + 1);

      await expect(governanceHub.connect(voter1).executeProposal(0))
        .to.be.revertedWith("Not execution authority");
    });
  });

  describe("Quorum enforcement", function () {
    it("should enforce quorum with mixed votes", async function () {
      await governanceHub.createProposal("Quorum test", VOTING_DURATION);

      await governanceHub.connect(voter1).vote(0, true);
      await governanceHub.connect(voter2).vote(0, false);
      await governanceHub.connect(voter3).vote(0, true);

      await time.increase(VOTING_DURATION + 1);

      // Total votes (3) >= quorum (3), should pass
      await expect(governanceHub.connect(executionAuthority).executeProposal(0))
        .to.emit(governanceHub, "ProposalExecuted");
    });
  });

  async function getDeadline(duration) {
    const block = await ethers.provider.getBlock("latest");
    return block.timestamp + duration;
  }
});
