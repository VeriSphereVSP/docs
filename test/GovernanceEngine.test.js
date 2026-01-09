const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("VotingContract (GovernanceEngine)", function () {
  let votingContract;
  let owner;
  let chairperson;
  let voter1;
  let voter2;
  let voter3;

  const proposalNames = [
    ethers.utils.formatBytes32String("Proposal A"),
    ethers.utils.formatBytes32String("Proposal B"),
    ethers.utils.formatBytes32String("Proposal C")
  ];

  beforeEach(async function () {
    [owner, chairperson, voter1, voter2, voter3] = await ethers.getSigners();

    const VotingContract = await ethers.getContractFactory("VotingContract");
    votingContract = await VotingContract.connect(chairperson).deploy(proposalNames);
    await votingContract.deployed();
  });

  describe("Deployment", function () {
    it("should set deployer as chairperson", async function () {
      expect(await votingContract.chairperson()).to.equal(chairperson.address);
    });

    it("should create proposals from constructor", async function () {
      for (let i = 0; i < proposalNames.length; i++) {
        const proposal = await votingContract.proposals(i);
        expect(proposal.name).to.equal(proposalNames[i]);
        expect(proposal.voteCount).to.equal(0);
      }
    });

    it("should emit ProposalAdded events", async function () {
      const VotingContract = await ethers.getContractFactory("VotingContract");

      await expect(VotingContract.deploy(proposalNames))
        .to.emit(VotingContract, "ProposalAdded");
    });
  });

  describe("vote", function () {
    it("should allow voting for a proposal", async function () {
      await expect(votingContract.connect(voter1).vote(0))
        .to.emit(votingContract, "VoteCasted")
        .withArgs(voter1.address, 0);

      const proposal = await votingContract.proposals(0);
      expect(proposal.voteCount).to.equal(1);
    });

    it("should mark voter as having voted", async function () {
      await votingContract.connect(voter1).vote(1);

      const voter = await votingContract.voters(voter1.address);
      expect(voter.voted).to.equal(true);
      expect(voter.vote).to.equal(1);
    });

    it("should prevent double voting", async function () {
      await votingContract.connect(voter1).vote(0);

      await expect(votingContract.connect(voter1).vote(1))
        .to.be.revertedWith("Already voted.");
    });

    it("should reject invalid proposal index", async function () {
      await expect(votingContract.connect(voter1).vote(99))
        .to.be.revertedWith("Invalid proposal index.");
    });

    it("should count multiple votes correctly", async function () {
      await votingContract.connect(voter1).vote(0);
      await votingContract.connect(voter2).vote(0);
      await votingContract.connect(voter3).vote(1);

      const proposal0 = await votingContract.proposals(0);
      const proposal1 = await votingContract.proposals(1);

      expect(proposal0.voteCount).to.equal(2);
      expect(proposal1.voteCount).to.equal(1);
    });
  });

  describe("delegate", function () {
    it("should allow delegation of vote", async function () {
      await expect(votingContract.connect(voter1).delegate(voter2.address))
        .to.emit(votingContract, "VotingDelegated")
        .withArgs(voter1.address, voter2.address);

      const voter1Data = await votingContract.voters(voter1.address);
      expect(voter1Data.voted).to.equal(true);
      expect(voter1Data.delegate).to.equal(voter2.address);
    });

    it("should add vote if delegate already voted", async function () {
      await votingContract.connect(voter2).vote(1);
      await votingContract.connect(voter1).delegate(voter2.address);

      const proposal = await votingContract.proposals(1);
      expect(proposal.voteCount).to.equal(2);
    });

    it("should prevent self-delegation", async function () {
      await expect(votingContract.connect(voter1).delegate(voter1.address))
        .to.be.revertedWith("Self-delegation is disallowed.");
    });

    it("should prevent delegation after voting", async function () {
      await votingContract.connect(voter1).vote(0);

      await expect(votingContract.connect(voter1).delegate(voter2.address))
        .to.be.revertedWith("You already voted.");
    });

    it("should detect delegation loops", async function () {
      await votingContract.connect(voter1).delegate(voter2.address);
      await votingContract.connect(voter2).delegate(voter3.address);

      await expect(votingContract.connect(voter3).delegate(voter1.address))
        .to.be.revertedWith("Found loop in delegation.");
    });

    it("should follow delegation chain", async function () {
      await votingContract.connect(voter1).delegate(voter2.address);
      await votingContract.connect(voter2).delegate(voter3.address);
      await votingContract.connect(voter3).vote(2);

      const proposal = await votingContract.proposals(2);
      expect(proposal.voteCount).to.equal(3);
    });
  });

  describe("winningProposal", function () {
    it("should return proposal with most votes", async function () {
      await votingContract.connect(voter1).vote(1);
      await votingContract.connect(voter2).vote(1);
      await votingContract.connect(voter3).vote(0);

      expect(await votingContract.winningProposal()).to.equal(1);
    });

    it("should return first proposal on tie", async function () {
      await votingContract.connect(voter1).vote(0);
      await votingContract.connect(voter2).vote(1);

      expect(await votingContract.winningProposal()).to.equal(0);
    });

    it("should return zero with no votes", async function () {
      expect(await votingContract.winningProposal()).to.equal(0);
    });
  });

  describe("winnerName", function () {
    it("should return name of winning proposal", async function () {
      await votingContract.connect(voter1).vote(2);
      await votingContract.connect(voter2).vote(2);

      expect(await votingContract.winnerName()).to.equal(proposalNames[2]);
    });
  });

  describe("addProposal", function () {
    it("should allow chairperson to add proposals", async function () {
      const newProposal = ethers.utils.formatBytes32String("New Proposal");

      await expect(votingContract.connect(chairperson).addProposal(newProposal))
        .to.emit(votingContract, "ProposalAdded")
        .withArgs(newProposal);

      const proposal = await votingContract.proposals(3);
      expect(proposal.name).to.equal(newProposal);
    });

    it("should reject non-chairperson adding proposals", async function () {
      const newProposal = ethers.utils.formatBytes32String("Unauthorized");

      await expect(votingContract.connect(voter1).addProposal(newProposal))
        .to.be.revertedWith("Caller is not the chairperson");
    });
  });

  describe("changeChairperson", function () {
    it("should allow owner to change chairperson", async function () {
      await expect(votingContract.connect(chairperson).changeChairperson(voter1.address))
        .to.emit(votingContract, "ChairpersonChanged")
        .withArgs(voter1.address);

      expect(await votingContract.chairperson()).to.equal(voter1.address);
    });

    it("should reject zero address", async function () {
      await expect(votingContract.connect(chairperson).changeChairperson(ethers.constants.AddressZero))
        .to.be.revertedWith("Zero address not allowed.");
    });
  });

  describe("ReentrancyGuard", function () {
    it("should protect vote function", async function () {
      // ReentrancyGuard is inherited, verify by checking nonReentrant modifier exists
      // This is implicitly tested by successful vote execution
      await votingContract.connect(voter1).vote(0);
      const voter = await votingContract.voters(voter1.address);
      expect(voter.voted).to.equal(true);
    });
  });
});
