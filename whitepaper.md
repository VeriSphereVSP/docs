# VeriSphere: A Game of Staked Truth  
### White Paper — v13.2 (Avalanche Edition, Draft)  
**Date:** January 2026  
**Contact:** info@verisphere.co  
**Discord** https://discord.gg/bzAdzceK

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

- Any player may publish a single atomic assertion (“Post”).
- Each Post must contain only one claim.
- Publishing a Post requires a small posting fee, denominated in VSP and pegged to a fixed quantity of gold at protocol launch.
- A Post begins at Verity Score (VS) = 0 until total stake on the Post (support or challenge) reaches at least the posting fee.
- The posting fee does not earn yield, but does count toward total stake once stake ≥ posting fee.
- Posts cannot be edited. Corrections must be made by posting a new Post and linking it.

The posting fee exists solely to discourage spam and low-commitment assertions.
It is designed to remain economically stable over time, independent of token price fluctuations.

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

## 3.5 Annualized Staking Rate (Revised)

Each stake earns or loses value continuously according to an annualized rate
determined by four factors:

1. **Queue Position** — earlier stakes receive greater exposure.
2. **Post Size** — stakes on larger claims experience greater pressure.
3. **Truth Pressure (VS)** — stronger consensus produces stronger economic force.
4. **Governed Bounds** — all rates stay between a minimum and maximum annual rate.

Let:

- `q_i` = the stake’s queue index (last = 1, earliest = Q_max)
- `Q_max` = the largest queue index of any active post
- `p_i` = total stake on the Post on the same side as stake `i`
- `P_max` = maximum post size among all active Posts
- `VS` = the Post’s Verity Score, in the range [-100, +100]
- `v = abs(VS) / 100` = normalized truth-pressure
- `r_max = 1.00` = maximum annual rate (100%)
- `r_min = 0.01` = minimum annual rate (1%)

### Annualized Rate

The annualized rate for stake `i` is:

```text
r_i = max(
    r_min,
    r_max
      * (q_i / Q_max)      # queue factor
      * (p_i / P_max)      # post-size factor
      * (abs(VS) / 100)    # truth-pressure factor
)
```

Interpretation:

- Earlier, larger stakes receive higher potential gains and higher potential burns.
- Posts with strong consensus (`|VS|` near 100) exert greater economic pressure.
- Posts with contested truth (`VS` near 0) exert minimal pressure.
- Every stake receives at least the minimum annualized exposure (`r_min`).

### Per-Step Balance Change

Let `sgn = +1` if the stake’s side matches the sign of `VS`,
and `sgn = -1` otherwise.

For a time step `Δt` in years:

```text
Δn = n * r_i * Δt * sgn
```

Stake update:

```text
n_next = max(0, n + Δn)
```

This produces symmetric gains and losses:

- Correct early stake on large claims earns the most.
- Incorrect early stake burns the most.
- Late stake bears less risk and less reward.
- VS determines the strength of the pressure.

### 3.6 Intuition & Economic Dynamics

- Early correct conviction earns most.  
- Early wrong conviction loses most.  
- Late entries face lower risk & lower reward.  
- Weak claims can be overturned via capital challenge.  
- Strong true claims become economically “fortified.”  
- Strong false claims leak value until corrected.  

### 3.7 Launch Parameters (governance-changeable)

- **Max staking rate:** 100% APR  
- **Min staking rate:** 1% APR  
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

### Effective VS Boundaries

Effective Verity Score is always clamped to the range [-100, +100].

Recursive propagation:
- Preserves sign
- Conserves total influence mass
- Terminates safely due to acyclic graph constraints

This prevents runaway amplification while still allowing deep evidence chains to matter economically.

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

### 5.2 Influence Calculation (Revised)

Evidence links do not simply add raw stake to a dependent claim.  
Instead, influence is **economically mediated** by:

1. The truth strength of the independent claim (IC)
2. The economic commitment on the link itself
3. The total economic mass of the IC
4. The number and strength of competing outgoing links from the IC

This ensures that:
- Foundational claims are economically protected
- Influence cannot be duplicated infinitely
- Players are incentivized to defend upstream postulates
- Flat, disconnected claim graphs are disfavored

Let:

- `IC` = Independent Claim  
- `DC` = Dependent Claim  
- `L` = a specific link from IC → DC  

Definitions:

- `VS(IC)` = effective Verity Score of IC, in range [-100, +100]  
- `VS(L)` = Verity Score of the link post itself, in range [-100, +100]  
- `T(IC)` = total stake on IC (support + challenge)  
- `T(L)` = total stake on link L  
- `ΣT(L_IC)` = sum of total stake over **all outgoing links** from IC  

A link contributes influence **only if**:

- IC has total stake ≥ posting fee  
- DC has total stake ≥ posting fee  
- The link itself has total stake ≥ posting fee  

Otherwise, the link contributes zero influence.

Circular references are prohibited.

Influence propagation is bounded, sign-preserving, and economically conserved.
No claim can amplify downstream influence beyond its own truth-weighted stake.

### 5.3 Link-Weighted IC Mass Distribution

Each claim possesses a finite amount of **economic influence mass**, derived from its own stake and truth strength.  
This mass is **not duplicated** across links — it is **distributed** among them.

#### Step 1: Compute IC Economic Mass

Define the *economic mass* of an independent claim:

$`M(IC) = VS(IC) × T(IC)`$

Where:
- `VS(IC)` is normalized to the range [-1, +1]
- `T(IC)` is the total stake on IC

This represents how much *truth-weighted capital* the claim carries.

#### Step 2: Compute IC Distribution Unit

Let:

$`U(IC) = M(IC) / ΣT(L_IC)`$

Where:
- `ΣT(L_IC)` is the sum of total stake across **all outgoing links** from IC

This defines the **unit of distributable influence per unit of link stake**.

> Intuition:  
> The more links compete to use an IC as evidence, the thinner its influence is spread — unless players reinforce specific links economically.

#### Step 3: Compute Link Contribution to DC

For a given link `L` from IC → DC:

$`Contribution(L → DC) = VS(L) × T(L) × U(IC)`$

Where:
- `VS(L)` reflects support or challenge polarity
- Challenge links invert sign automatically

This value is added to the **effective Verity Score accumulator** of the dependent claim.

#### Properties

This mechanism guarantees:

- **Conservation of influence** — IC influence cannot be multiplied
- **Defense incentive** — players must protect upstream claims
- **Selective reinforcement** — strong links matter more than weak ones
- **Resistance to spam linking** — low-stake links dilute themselves

---

## 6. Tokenomics (VSP)

| Property | Description |
|---------|-------------|
| Supply | Elastic: minted for correct stakes, burned for wrong stakes |
| Posting fee | Denominated in VSP, normalized to a fixed gold reference |
| Reserve mechanics | None — market-driven value |
| Treasury | For bounties & bootstrap, transparent on-chain (Avalanche) |

Economic equilibrium emerges through **risk, skill, and truth-seeking behavior**.

### 6.1 Gold Reference & Economic Normalization

VeriSphere uses a gold reference solely as a normalization anchor for certain protocol thresholds.

**Gold is not used to price truth, stake outcomes, or Verity Scores.**

Specifically:

- Posting fees are defined as a fixed fraction of a troy ounce of gold at protocol launch.
- This reference is used only to:
- - Maintain a consistent real-world cost for posting claims over time
  - Prevent inflation or deflation of spam resistance as VSP’s market price changes
- The protocol may consult a widely available gold price oracle to translate this fixed gold reference into an equivalent amount at the time of posting.

Importantly:

- Verity Score (VS) is dimensionless. It depends only on relative stake proportions, not absolute value.
- Stake competition is internal. All rewards, burns, and redistributions occur purely in VSP.
- Truth discovery does not depend on the oracle. If oracle data is unavailable, existing stakes and VS calculations continue unaffected.

Gold serves the same role as a unit constant —
like a meter or a second — not as an external arbiter of truth.

Governance may update oracle sources or normalization parameters over time, but such changes do not retroactively affect historical outcomes or VS comparisons.

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

- Modify protocol parameters (posting fee factor, yield bands, staking rate parameters)  
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

- **VSP Token (Solidity):** ERC-20 compatible token with governance-controlled mint and burn hooks.  
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
