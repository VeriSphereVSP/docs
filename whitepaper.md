# VeriSphere: A Game of Staked Truth  
### White Paper — v13.0 (Avalanche Edition, Draft)  
**Date:** November 2025  
**Contact:** info@verisphere.co  

---

## Abstract

**VeriSphere is a truth‑staking game — a competitive market where belief carries financial consequence.**  
Any player may publish a factual claim, and any player may stake VSP tokens to support or challenge it. When you're right, your stake grows; when you're wrong, you lose. Over time, truthful claims accumulate economic weight, while false or unsupported claims lose it.

Players strengthen claims by linking evidence, challenging weak assertions, and participating in a dynamic, adversarial epistemic market. No moderators, no upvotes, no reputation — **only transparent rules, incentives, and skin in the game.**

VeriSphere is both a protocol and a public knowledge engine: a decentralized mechanism for lifting truth and sinking misinformation by aligning economic incentives with intellectual honesty.

---

## 1. Vision & Motivation

Information systems today are failing. Search engines prioritize engagement over accuracy. Social platforms amplify outrage and misinformation. “Fact-checking” systems are centralized and opaque. Knowledge repositories like Wikipedia rely on volunteer moderation, subjective consensus, and often fragile social dynamics. Prediction markets offer rigor, but only around events with binary, terminal outcomes — not open-ended questions, evolving topics, or foundational factual claims.

In short: **there is no global, game-theoretic system that rewards truth and penalizes falsehood at scale**.

### Problems With Existing Systems

#### 1) No Cost to Being Wrong

Online, false claims spread freely. There is typically **no economic or reputational cost** for asserting misinformation — and often a reward for virality over accuracy. Meanwhile, being correct yields little beyond internet points. Outcome: **no meaningful disincentive to be wrong, no reward for truth-seeking**.

#### 2) Popularity ≠ Truth

Algorithms surface content based on clicks, emotions, and tribal alignment, not correctness. Influence is earned through **volume and charisma, not accuracy**. Upvotes and likes create **echo chambers**, not validated knowledge.

#### 3) Centralized Moderation & Editorial Bias

Platforms rely on moderation teams, committees, or opaque rules. Even Wikipedia’s “neutrality” is mediated by human gatekeepers. These systems are vulnerable to:

- Elite capture  
- Editorial bias and agenda setting  
- Ideological enforcement  
- Social pressure, brigading, and narrative control  

There is no trustless mechanism to ensure neutrality.

#### 4) Prediction Markets Stop Too Soon

Prediction markets are powerful truth machines — but they focus on **finite, resolvable events**. They cannot persistently evaluate claims like:

- “Nuclear energy is environmentally sustainable”  
- “Quantum encryption defeats classical surveillance”  
- “Ketogenic diets improve long-term metabolic health”  

Truth evolves; **most knowledge does not resolve cleanly**. Current markets cannot handle ongoing, evidence-driven veracity.

#### 5) Knowledge Is Fragmented & Hard to Verify at Source

Wisdom exists across Wikipedia, academic papers, open-source communities, forums like Reddit and StackExchange, long-form content, and specialist communities. Yet it is scattered, hard to verify, and **not economically integrated**. No system incentivizes:

- Surfacing the most accurate information  
- Challenging weak claims  
- Linking evidence rationally  
- Updating truth dynamically  

### Opportunity

There is a unique moment to build a **game-theoretic knowledge engine** where:

- Claims compete in an open market of proof and challenge  
- Stake, not status, determines influence  
- Truth accretes economic weight  
- Falsehood burns capital  
- Evidence chains are transparent, inspectable, and immutable  
- Incentives favor intellectual honesty over virality  

### Vision

VeriSphere re-engineers online knowledge around **accountable speech**:

> Put your money where your mouth is — and earn for being right.

The system is **not** a forum, **not** a social network, and **not** a traditional governance DAO.

It is a **truth-staking market** — a competitive game where epistemology meets economics.

The goal is not consensus. It is **truth-pressure**.  
The winner is not the loudest voice — but the most correct one, over time.

VeriSphere aims to become:

- A global contest of ideas  
- A public map of truth pressure  
- A financially-backed epistemic graph  
- A market-driven defense against misinformation  
- A foundation layer for AI training and validation  

In a world of noise and narrative, VeriSphere introduces **economic gravity** to truth.

---

## 2. System Overview

VeriSphere is a truth-staking protocol where information is expressed as **atomic claims**, called *posts*. Each post is a single, standalone assertion stated as clearly and conclusively as possible — no narrative, no multi-point arguments, no hedging.

Examples:

- “Vaccines reduce the risk of severe COVID-19.”  
- “Nuclear energy is safer per kWh than coal.”  
- “Ethereum will surpass Bitcoin in market capitalization.”

Every post is a discrete unit of truth-competition.

### Posting

Any player can publish a new claim.  
Publishing burns a small fee, ensuring posts represent meaningful assertions rather than noise.

Posts are immutable — if a user wishes to revise or clarify, they publish a **new post** and may link it to the original.

### Supporting & Challenging

Players stake VSP to either:

- **Support** a post (assert the claim is true, or directionally correct)  
- **Challenge** a post (assert the claim is false, misleading, overstated, or wrong)  

Outcome:

- If you're aligned with the long-term truth consensus, your stake grows.  
- If you're wrong, your stake shrinks or is burned.

Supporting a claim is akin to saying:

> “I believe this is true — confidently enough to risk capital.”

Challenging a claim means:

> “I believe this is false — and I'm willing to bet against it.”

### Linking Evidence in Context

Discussion is not free-form argumentation.  
**Comments are themselves claims**.

When you “comment” on a post, you are creating (or referencing) another atomic post and **linking it as evidence**:

- Support link: strengthens the parent post  
- Challenge link: undermines the parent post  

Example:

- Post A: “Nuclear energy has the lowest mortality per kWh.”  
- Post B: “Data from Our World in Data confirms nuclear fatalities are lowest per TWh.”

If a user links B → A as support:

- B becomes **evidence** for A.  
- B’s own Verity Score and stake influence A.

Each link has its own stake and can itself be supported or challenged, meaning:

- Posts have independent truth scores  
- Links have independent credibility  
- Contextual links combine with standalone truth to calculate influence  

This creates a **web of evidence**, rather than a comment section.

### Continuous Truth Pressure

Posts never “resolve.”  
Truth emerges over time — not by vote but by **economic competition**.

- Strong claims accumulate capital, evidence, and network reinforcement  
- Weak claims lose stake and visibility  
- New evidence can overturn long-held beliefs  
- All incentives favor clarity, precision, and accountability  

VeriSphere is a **market for truth**, where the scoreboard is capital at risk and correctness over time.

---

## 3. Posting & Staking Mechanics

### 3.1 Posting

- Any player may publish a single **atomic assertion** (“Post”).  
- Each Post must contain only **one claim**.  
- Publishing a Post requires a **gold-pegged fee** (burned).  
- A Post begins at **Verity Score (VS) = 0** until total stake on the Post (support or challenge) reaches at least the posting fee.  
- The posting fee **does not earn yield**, but **does count toward total stake once stake ≥ posting fee**.  
- Posts cannot be edited. Corrections must be made by posting a new Post and linking it.

### 3.2 Staking on Claims

Players may stake VSP to:

- **Support** a Post (assert it is true), or  
- **Challenge** a Post (assert it is false)  

Stake can be:

- Added incrementally  
- Withdrawn (affecting queue position)  
- Flipped between support and challenge  

Stakes **earn or lose value** depending on alignment with the Post’s Verity Score (VS).

### 3.3 Verity Score (VS)

The Verity Score reflects consensus truth-belief in a Post.

Let:

- $`A`$ = total support stake  
- $`D`$ = total challenge stake  
- $`T = A + D`$

Then:

$`VS = (2 \times (A / T) - 1) \times 100`$

Range:

- **+100** = universally believed true  
- **0** = unclear / contested  
- **−100** = universally believed false  

VS updates continuously as stakes move.

### 3.4 Positional Staking System

Stake on each side forms a **queue** by arrival time.

Principles:

- Earlier stake receives **higher reward when right** and **higher penalty when wrong**.  
- Later stake receives **lower reward** and **lower penalty**.  
- Removing stake causes later stake to **shift forward** into earlier, riskier positions.

Incentives:

- Honest early conviction  
- Discouraging passive “wait-to-snipe” behavior  
- Ability to flip false claims with capital  
- Meaningful commitment to defend claims  

### 3.5 Yield and Burn Mechanics (Formal Definitions)

Let:

- $`n`$ = your stake amount  
- $`\Delta t`$ = time step (years)  
- $`VS \in [-100, +100]`$  
- $`v = |VS| / 100`$  
- $`T`$ = total stake on the Post (support + challenge)  
- $`side \in \{\text{support}, \text{challenge}\}`$  
- $`sgn = +1`$ if your side matches `sign(VS)`, $`-1`$ if opposite, $`0`$ if $`VS = 0`$  
- $`R_{max}`$ = governed maximum annual rate (e.g., 10 × US10Y)  
- $`R_{min}`$ = governed minimum annual rate (e.g., 0.1 × US10Y)  

#### Maturity Parameter

Let:

- $`S`$ = total VSP supply  
- $`A`$ = number of active Posts (stake ≥ posting fee)  

Then:

$`K = S / A`$  (if $`A = 0`$, define $`K = S`$)

Maturity function:

$`f(T) = T / (T + K)`$

Interpretation: deeper, more engaged claims earn nearer the max rate.

#### Effective Annual Rate

$`r_{eff} = R_{min} + (R_{max} - R_{min}) \times v \times f(T)`$

- If $`VS = 0`$, then $`v = 0 \Rightarrow r_{eff} = R_{min}`$  
- If $`|VS| = 100`$ and $`T \gg K`$, then $`r_{eff} \approx R_{max}`$

#### Positional Weighting

Let $`i = 1`$ be the earliest stake position on your side.  
Weight per position:

$`w_i = \dfrac{1 / i}{\sum_{j=1}^{N_s} (1 / j)}`$

Where $`N_s`$ = number of stake lots on that side.

- Position 1 has the strongest effect.  
- When earlier lots withdraw, later lots shift forward.

#### Per-step Change in Stake

If $`VS = 0`$ or $`T < \text{postingFee}`$:

$`\Delta n = 0`$

Else:

$`\Delta n = n \times sgn \times w_i \times r_{eff} \times \Delta t`$  
$`n_{next} = \max(0, n + \Delta n)`$

- Aligned stake grows  
- Misaligned stake burns  
- Early stake feels the strongest effect  

### 3.6 Intuition & Economic Dynamics

- Early correct conviction earns most.  
- Early wrong conviction loses most.  
- Late entries face lower risk & lower reward.  
- Weak claims can be overturned via capital challenge.  
- Strong true claims become economically “fortified.”  
- Strong false claims leak value until corrected.  

### 3.7 Launch Parameters (governance-changeable)

- **Max staking rate:** 10× US 10-Year Treasury  
- **Min staking rate:** 0.1× US 10-Year Treasury  
- **K formula:** $`K = S / A`$ (with $`A`$ = active Posts)  

---

## 4. Verity Score Mechanics

### 4.1 Base Verity Score (no links)

Let:

- $`A`$ = total support stake  
- $`D`$ = total challenge stake  
- $`T = A + D`$  

Base Verity Score:

$`VS = (2 \times (A / T) - 1) \times 100`$

Clamped to **−100 to +100**.  
Neutral until total stake ≥ posting fee.

---

## 5. Evidence Links Between Claims

### 5.1 Relation Definition

A **Relation** is a directed link from one claim to another:

- **Support** (strengthens parent claim)  
- **Challenge** (weakens parent claim)  

Let:

- Claim $`S`$ supports or challenges claim $`A`$  
- Stake on relation inside this context = $`R_{ctx}`$  
- Independent stake on $`S`$ = $`S_{total}`$  

### 5.2 Influence Calculation

Normalize S Verity Score to [0,1]:

$`nVS(S) = (BaseVS(S) + 100) / 200`$

Contribution to A:

- **Support:** adds $`nVS(S) \times R_{ctx}`$ to effective support on A  
- **Challenge:** adds $`nVS(S) \times R_{ctx}`$ to effective challenge on A  

Total “effective” support and challenge for A:

- $`A_{support} += nVS(S) \times R_{ctx}`$ (for support links)  
- $`A_{challenge} += nVS(S) \times R_{ctx}`$ (for challenge links)  

Circular references are prohibited.

---

## 6. Tokenomics (VSP)

| Property | Description |
|---------|-------------|
| Supply | Elastic: minted for correct stakes, burned for wrong stakes |
| Initial peg | $`1 \text{ VSP} = \$1`$ at launch |
| Posting fee | Pegged to $`1/4000`$ oz of gold via oracle |
| Reserve mechanics | None — market-driven value |
| Treasury | For bounties & bootstrap, transparent on-chain (Avalanche) |

Economic equilibrium emerges through **risk, skill, and truth-seeking behavior**.

---

# 7. Governance Lane (“GP” Namespace)

## 7.0 Overview

Truth discovery and protocol stewardship must coexist but operate under fundamentally different rules.  
VeriSphere therefore defines two parallel, interoperable lanes:

- **Knowledge Claims (KC):** perpetual, open-ended truth-staking market  
- **Governance Proposals (GP):** time-bounded, executable protocol decisions  

KC maintains epistemic integrity (“truth never finalizes”).  
GP provides operational finality (“decisions must finalize”).  
Together they form a self-evolving truth economy that governs itself through explicit, auditable actions.

---

## 7.1 Governance Goals

Governance exists to:

- Maintain and evolve core protocol parameters  
- Approve upgrades, treasury allocations, and ecosystem changes  
- Support community bounties and ecosystem expansion  
- Preserve long-term credibility and security  

Governance is **minimally interventionist**; the truth market must remain primary.

---

## 7.2 GitHub-Based Proposal Lifecycle (Operational Implementation)

During the MVP phase, the **Governance Lane** operates through GitHub’s native structures integrated with the on-chain bounty system (on Avalanche).

Each **GitHub Issue** in the `VeriSphere/docs` repository represents a **Governance Proposal Object (GPO)** or **bounty task**.

### Lifecycle

1. **Draft**  
   - Anyone may draft a proposal as a GitHub Issue.  
   - The issue contains title, description, dependencies, and deliverables.  

2. **Activation / Bounty Definition**  
   - The issue is labeled `bounty` plus a phase label (`phase:1`, etc.) and status label (`status:planned`).  
   - A reward (in VSP) is encoded in the issue body (`Bounty: NNNN`).  
   - A GitHub Action syncs the issue into a Google Sheets “bounty ledger” that acts as a transparent off-chain index.

3. **Approval**  
   - A designated governance multisig or role (on Avalanche) approves the task by updating on-chain bounty state to match the ledger.  
   - The bounty amount becomes reserved in the on-chain treasury contract.

4. **Execution / Work**  
   - Contributors implement the task (code, docs, infra).  
   - Evidence of completion: PRs, commits, deployments, audits.  

5. **Review & Finalization**  
   - Reviewers validate that deliverables meet acceptance criteria.  
   - If accepted, a payout transaction is sent from the on-chain bounty pool to the contributor.

6. **Completion & Logging**  
   - The GitHub Issue is updated with the Avalanche transaction ID:  
     `$`TxID (Avalanche Explorer URL)`$`  
   - The Google Sheet row is updated with status and TxID.  
   - The issue is closed and acts as an immutable governance record.

This model turns ordinary GitHub issues into **governance proposals and bounty contracts**, linking operational transparency with economic finality on Avalanche.

---

## 7.3 Reward Curve (Economic Governance Model)

Bounty emissions follow a **governance-defined reward curve** that compensates early protocol labor more heavily than late-stage work.

The per-hour reward function is:

$`r(n) = 100 + (100000 - 100) \times e^{-k(n-1)}`$

where:

$`k = \dfrac{\ln((100000 - 100)/\varepsilon)}{H - 1}, \quad \varepsilon = 1`$

and:

- $`H`$ = total pre-MVP cumulative hours.  
- $`n`$ = the $`n`$-th hour of total pre-MVP effort (ordered across tasks).

Interpretation:

- The **first** pre-MVP hour earns ≈ `100000 VSP`  
- The **last** pre-MVP hour earns ≈ `100 VSP`  
- Rewards decline smoothly and continuously as the protocol matures.

Each task receives a **bounty** equal to the sum of rewards for its hour range:

$`\text{Bounty(Task)} = \sum_{n = N_{start}}^{N_{end}} r(n)`$

For each task, the computed bounty is **hard-coded into the GitHub Issue body** (e.g., `Bounty: 29184258`) and mirrored in the sheet. The CI pipeline does **not** recompute rewards; it reads them from the Issue and treats them as canonical.

Governance may, in later epochs, propose updates to:

- $`R_{max}`$  
- $`R_{min}`$  
- $`\varepsilon`$  
- Post-MVP reward curves  

but pre-MVP bounties remain **fixed** once published.

---

## 7.4 Quorum, Thresholds, and Safeguards

Formal on-chain governance (post-MVP) inherits these safeguards:

- **Quorum requirement:** minimum voting participation (by stake or Cred Score)  
- **Approval threshold:** simple or super-majority for passage  
- **Turnout guardrails:** prevent low-participation capture  
- **Proposal deposit / bond:** prevents spam; refundable if proposal meets quality thresholds  
- **Emergency controls:** circuit breaker, extended timelocks, or veto in case of critical bugs  

During MVP, multisig-based approval of issues acts as a conservative stand-in for on-chain quorum.

---

## 7.5 Executable Authority (Avalanche EVM)

Executed proposals can:

- Modify protocol parameters (posting fee factor, yield bands, decay rates)  
- Manage treasury funds (grants, bounties, ecosystem incentives)  
- Authorize upgrades to core Solidity contracts and APIs (using proxy patterns)  
- Assign or revoke governance roles in upgrade controllers  
- Approve new modules (e.g., oracles, bridges, identity layers)  

All actions are implemented as **EVM transactions** on Avalanche:

- Either on the **Avalanche C-Chain**, or  
- On a dedicated **Avalanche Subnet** reserved for VeriSphere.

---

## 7.6 Interaction With KC Lane

Knowledge staking and governance are related but distinct:

- KC stakes do **not** automatically count as GP voting power unless explicitly included in the voting formula.  
- KC outcomes **do not** directly force protocol changes (truth ≠ enactment).  
- GP can modify KC **parameters** (e.g., posting fees, yield bands) but cannot decree the truth or falsity of specific claims.

This separation preserves **epistemic independence** and **market integrity**.

---

## 7.7 Proposal Types

Common governance proposal classes:

- **Parameter changes:** posting fee factor, yield bands, decay rates, VS thresholds  
- **Treasury allocations:** research grants, onboard bounties, community programs  
- **Protocol upgrades:** new staking primitives, graph optimizations, Subnet changes  
- **Infrastructure tasks:** indexer improvements, AI-assist modules, data pipelines  
- **Emergency responses:** halt or mitigation responses, security patches  

All begin as **GitHub issues** and, upon funding, become GP objects executed on Avalanche.

---

## 7.8 Governance UI and UX

To maximize legitimacy:

- Proposal templates and issue forms  
- On-chain and off-chain metadata alignment  
- Impact visualization and code diffs (before/after)  
- Voting guides and simulation tools  
- Public audit trails and vote receipts  
- Wallet integration for on-chain voting (post-MVP)  

---

## 7.9 Economic Safeguards

To protect against governance capture:

- **Proposal bonds** to discourage frivolous governance  
- **Staged treasury access:** streaming, vesting, and per-epoch caps  
- **Slashing or lock-ups** for malicious attempts  
- **Idle decay** on unspent governance allocations, redirecting them back to a reserve pool  

Economic resistance complements social consensus and contract security.

---

## 7.10 Summary

The Governance Lane enables verifiable, time-bounded, executable decision-making without contaminating the perpetual truth-staking market.

- KC discovers truth.  
- GP steers the protocol.  

Both use VSP, both are transparent — but only GP **finalizes and executes**.

---

## 8. Architecture (Avalanche Edition)

| Layer | Components | Notes |
|-------|------------|-------|
| Core Protocol | Solidity contracts: Posts, Stakes, VS logic, LinkGraph, VSP token, Treasury, Governance | Deployed on Avalanche C-Chain or VeriSphere Subnet |
| Indexing | Event log indexers, graph builders, history stores | Off-chain, read-optimized |
| API | REST / GraphQL, WebSocket feeds | Public, read-only |
| Clients | Official UI + 3rd-party front-ends | Permissionless |
| AI Assist (optional) | Semantic search, decomposition, summarization | Off-chain |

**On-chain = rules + economics (Avalanche EVM).**  
**Off-chain = convenience + discovery.**

Core components:

- **VSP Token (Solidity):** ERC-20 compatible token with governance-controlled mint, burn, and idle-decay hooks.  
- **PostRegistry:** immutable Posts, posting fees, base VS logic.  
- **StakeEngine:** per-Post staking queues, reward/burn calculation, side flipping, withdrawal.  
- **LinkGraph:** support/challenge edges, cycle prevention, influence propagation.  
- **Treasury:** holds VSP, executes payouts under governance control.  
- **GovernanceHub:** handles proposals, state changes, and interactions with other contracts.

Avalanche-specific features (C-Chain or Subnet):

- Fast finality (sub-second) for interactive staking UX.  
- EVM compatibility enabling standard tools (Hardhat, Foundry, The Graph).  
- Optional Subnet for dedicated throughput and custom gas economics.

---

## 9. UI & Data Layer Separation

- Protocol = independent, composable, permissionless  
- UI = one of many possible front-ends  
- API supports 3rd-party apps, bots, analytics tools

Users should be able to build:

- Desktop clients  
- Mobile wallets  
- AI truth-check assistants  
- Research and monitoring tools  
- Anonymous CLI tools  

VeriSphere = **public truth engine + economic layer**, not a single website.

---

## 10. Roadmap

| Phase | Deliverables |
|-------|--------------|
| Alpha | Core Solidity contracts on Avalanche (VSP token, Posts, Stakes, Links) plus basic indexer |
| Beta | Governance contracts, expanded indexer, AI collation backend, encyclopedia-style UI |
| Launch | Public UI and docs, bounty system fully on-chain, open contribution program |
| Scale | Dedicated Avalanche Subnet (optional), AI-powered discovery, cross-chain read-oracles for other ecosystems |

---

## 11. Conclusion

VeriSphere introduces **economic truth-pressure**:  
A decentralized environment where correctness earns, falsehood costs, and evidence shapes outcomes.

A global, adversarial, transparent game of ideas —  
**where belief has consequence and truth has weight.**

---
