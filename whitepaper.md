# VeriSphere: A Game of Staked Truth  
### White Paper — v13.0 (Draft)  
**Date:** November 2025  
**Contact:** info@verisphere.co  

## Abstract

**VeriSphere is a truth-staking game — a place where belief meets consequence. It’s “put your money where your mouth is” applied to knowledge.**  
Any player can publish a claim — and **any player can stake on any claim**. If you believe a statement is true, you can support it with stake; if you think it’s false, you can challenge it. When you're right, you earn. When you're wrong, you lose.

Players challenge weak claims, support strong ones, and link evidence across the network to strengthen them. Claims that withstand real scrutiny rise in value and visibility; weak, false, or unsupported claims lose stake and fade.

There are no moderators, no reputation systems, no popularity contests — only transparent rules and economic incentives. VeriSphere is both a venue and a protocol for discovering truth and sinking misinformation, powered not by any central authority, but by **evidence, courage, and skin in the game**.

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

> *Put your money where your mouth is — and earn for being right.*

The system is **not** a forum, **not** a social network, and **not** a traditional governance DAO.

It is a **truth-staking market** — a competitive game where epistemology meets economics.

The goal is not consensus. It is **truth-pressure**.  
The winner is not the loudest voice — but the most correct one, over time.

VeriSphere aims to become:
- A **global contest of ideas**  
- A **public map of truth pressure**  
- A **financially-backed epistemic graph**  
- A **market-driven defense against misinformation**  
- A **foundation layer for AI training and validation**

In a world of noise and narrative, VeriSphere introduces **economic gravity** to truth.

---

## 2. System Overview

VeriSphere is a truth-staking protocol where information is expressed as **atomic claims**, called *posts*. Each post is a single, standalone assertion stated as clearly and conclusively as possible — no narrative, no multi-point arguments, no hedging. Examples:

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

- **Support** a post  
  (assert the claim is true, or directionally correct)

- **Challenge** a post  
  (assert the claim is false, misleading, overstated, or wrong)

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

Post A: “Nuclear energy has the lowest mortality per kWh.”

A user adds:

Post B: “Data from Our World in Data confirms nuclear fatalities are lowest per TWh.”

And links B → A as support.

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

The Verity Score reflects consensus truth-belief in a Post:

**VS = (2 × (support_stake ÷ total_stake) − 1) × 100**

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

- **n** = your stake amount
- **Δt** = time step (years)
- **VS ∈ [−100, +100]**
- **v = |VS| / 100**
- **T** = total stake on the Post (support + challenge)
- **side** ∈ {support, challenge}
- **sgn = +1** if your side matches sign(VS), **−1** if opposite, **0** if VS = 0
- **R_max** = governed maximum annual rate (e.g., 10 × US10Y)
- **R_min** = governed minimum annual rate (e.g., 0.1 × US10Y)

#### Maturity parameter

Let:

- **S** = total VSP supply
- **A** = number of active Posts (stake ≥ posting fee)

Then:

**K = S / A**  
(if A = 0, define K = S)

and maturity function:

**f(T) = T / (T + K)**

Interpretation: deeper, more engaged claims earn nearer the max rate.

#### Effective annual rate

**r_eff = R_min + (R_max − R_min) × v × f(T)**

- If **VS = 0**, then **v = 0 → r_eff = R_min**
- If **|VS| = 100** and **T >> K**, then **r_eff ≈ R_max**

#### Positional weighting

Let **i = 1** be earliest stake position on your side.  
Weight per position:

**w_i = (1 / i) ÷ Σ (1 / j) for j = 1…N_s**

(N_s = number of stake lots on that side)

- Position 1 has the strongest effect.
- When earlier lots withdraw, later lots shift forward.

#### Per-step change in stake

If **VS = 0** or **T < posting fee**:

**Δn = 0**

Else:

**Δn = n × sgn × w_i × r_eff × Δt**  
**n_next = max(0, n + Δn)**

- Aligned stake grows  
- Misaligned stake burns  
- Early stake feels the strongest effect

### 3.6 Unstaked Value Decay

Unstaked VSP decays at **R_min** per year:

**U_next = U × (1 − R_min × Δt)**

Purpose:

- Discourage “idle whale ambushes”
- Encourage active participation
- Sustain circulating engagement, not hoarding

### 3.7 Intuition & Economic Dynamics

- Early correct conviction earns most.
- Early wrong conviction loses most.
- Late entries face lower risk & lower reward.
- Weak claims can be overturned via capital challenge.
- Strong true claims become economically “fortified.”
- Strong false claims leak value until corrected.
- Holding idle capital erodes value, pushing engagement.

### 3.8 Launch Parameters (governance-changeable)

- **Max staking rate:** 10× US 10-Year Treasury
- **Min staking rate:** 0.1× US 10-Year Treasury
- **K formula:** K = S / A (with A = active Posts)

---
## 4. Verity Score Mechanics

### 4.1 Base Verity Score (no links)
Let:  
- **A** = total support stake  
- **D** = total challenge stake  
- **T** = A + D

Base Verity Score:  
<span style="font-family: monospace; font-size: 95%">
(2 × (A / T) − 1) × 100  
</span>  
Clamped to **−100 to +100**

Neutral until total stake ≥ posting fee.

---

## 5. Evidence Links Between Claims

### 5.1 Relation Definition
A **Relation** is a directed link from one claim to another:  
- **Support** (strengthens parent claim)  
- **Challenge** (weakens parent claim)  

Let:  
- Claim **S** supports or challenges claim **A**  
- Stake on relation inside this context = **R_ctx**  
- Independent stake on S = **S_total**  

### 5.2 Influence Calculation
Normalize S Verity Score to 0-1 scale:  
<span style="font-family: monospace; font-size: 95%">
nVS(S) = (BaseVS(S) + 100) / 200  
</span>

Contribution to A:  
- **Support:** adds `nVS(S) × R_ctx` to A  
- **Challenge:** subtracts `nVS(S) × R_ctx` from A

Total votes on A become:  
<span style="font-family: monospace; font-size: 95%">
A_support += (nVS(S) × R_ctx)  
A_challenge unchanged  
</span>  
(or vice-versa for challenge link)

Circular references prohibited.

---

## 6. Tokenomics (VSP)

| Property | Description |
|---|---|
Supply | Elastic: minted for correct stakes, burned for wrong stakes |
Initial peg | 1 VSP = $1 at launch |
Posting fee | Pegged to **1/4000 oz of gold** via oracle |
Unstaked VSP | Burns at minimum APR |
Reserve mechanics | None — market-driven value |
Treasury | For bounties & bootstrap, transparent on-chain |

Economic equilibrium emerges through **risk, skill, and truth-seeking behavior**.

---

# 7. Governance Lane (“GP” Namespace)

## 7.0 Overview
Truth discovery and protocol stewardship must coexist but operate under fundamentally different rules.  
VeriSphere therefore defines two parallel, interoperable lanes:

- **Knowledge Claims (KC):** perpetual, open-ended truth-staking market  
- **Governance Proposals (GP):** time-bounded, executable protocol decisions  

**KC** maintains epistemic integrity (“truth never finalizes”).  
**GP** provides operational finality (“decisions must finalize”).  
Together they form a self-evolving truth economy that governs itself through explicit, auditable actions.

---

## 7.1 Governance Goals
Governance exists to:

- Maintain and evolve core protocol parameters  
- Approve upgrades, treasury allocations, and ecosystem changes  
- Authorize community bounties and project expansions  
- Preserve long-term credibility, security, and incentive balance  

Governance is **minimally interventionist**:  
the **truth market** (KC lane) remains primary; the **governance lane** only adjusts the rules of the game and funds legitimate work supporting truth infrastructure.

---

## 7.2 GitHub-Based Proposal Lifecycle (Operational Implementation)

During the MVP phase, the **Governance Lane** operates through GitHub’s native structures integrated with the on-chain bounty system.  
Each **GitHub Issue** represents a **Governance Proposal Object (GPO)**.

### Lifecycle

| Stage | Description |
|--------|-------------|
| **Draft** | Any verified contributor opens a GitHub issue in the `verisphere/docs` repository.  The issue serves as a draft proposal with title, description, dependencies, and deliverables. |
| **Activation** | The issue receives a label `bounty:<amount>` and enters the Governance Project board.  A bounty escrow is automatically provisioned via the GitHub Action → Google Sheets → Solana flow. |
| **Voting / Approval** | Reviewers (multisig or governance wallet) mark the issue as `approved`.  This updates the bounty ledger and locks funds in the on-chain bounty contract. |
| **Execution / Work** | Contributors complete the deliverables.  Work is validated through PRs, commits, or deployed artifacts. |
| **Completion / Payout** | When verified, the GitHub Action writes the payout `$`TxID (Solscan)`$` to the bounty ledger.  The issue is closed and becomes permanent protocol history. |

This model turns ordinary GitHub issues into **on-chain governance proposals**, linking operational transparency with economic finality.

---

## 7.3 Reward Curve (Economic Governance Model)

Bounty emissions follow a **governance-defined reward curve** that compensates early protocol labor more heavily than late-stage maintenance.

The per-hour reward function is:

$`r(n) = 100 + (100{,}000 - 100) \times e^{-k(n-1)}`$

where  

$`k = \frac{\ln((100{,}000 - 100)/\varepsilon)}{H-1}, \quad \varepsilon = 1`$  

and  

$`H`$ = total pre-MVP cumulative hours.

Thus:

- the **first hour** of work earns ≈ **100 000 VSP / hour**, rewarding foundational research and architecture;  
- the **final pre-MVP hour** earns ≈ **100 VSP / hour**, reflecting stabilized maturity.

Each task’s bounty equals the **sum** of $`r(n)`$ across its hour range $`[N_{start}, N_{end}]`$.  
This ensures **fair temporal decay** and **predictable token emission** across development.

Governance can update the parameters $`r_0`$, $`r_{floor}`$, or $`\varepsilon`$ via future proposals, keeping reward policy transparent and algorithmically defined.

---

## 7.4 Quorum, Thresholds, and Safeguards
Formal on-chain governance (post-MVP) inherits these GP safeguards:

- **Quorum:** minimum stake participation for proposal validity  
- **Approval threshold:** majority / super-majority depending on impact  
- **Turnout guardrails:** prevent apathy or capture  
- **Proposal bond:** spam deterrent; refundable for qualified proposals  
- **Emergency controls:** circuit breaker, timelock extensions, vetoes  

Until full decentralization, multisig verification of GitHub issues acts as interim quorum enforcement, ensuring each bounty reflects community consensus.

---

## 7.5 Executable Authority
Approved proposals may:

- Modify protocol parameters (fees, yield, decay, quorum, etc.)  
- Allocate or burn VSP treasury funds  
- Upgrade smart-contracts / APIs  
- Define reward-curve constants  
- Approve new modules or oracles  
- Trigger audits or governance reviews  

All actions resolve on-chain—either as transactions through governance contracts or authenticated signatures in the off-chain ledger pipeline.

---

## 7.6 Interaction With KC Lane
Knowledge and governance remain distinct yet interoperable:

- KC staking outcomes influence **Cred Score**, which can weight GP voting.  
- GP outcomes never alter KC truth — truth cannot be voted on.  
- GP may modify KC parameters (e.g., posting fee factor) but not specific claim veracity.  

This preserves **epistemic independence** and **economic accountability**.

---

## 7.7 Proposal Types (Mapped to GitHub)

| Type | Example | Repository |
|------|----------|------------|
| **Parameter Change** | Adjust yield bands or decay rates | `core` |
| **Treasury Allocation** | Fund research grant / bounty pool | `docs` |
| **Protocol Upgrade** | Deploy new staking primitive | `core` |
| **Infrastructure Task** | Build AI collation backend | `backend` |
| **UI / UX Task** | Create encyclopedia frontend | `frontend` |
| **Emergency Response** | Temporary halt / patch | `core` |

All begin as GitHub issues (proposal drafts) and escalate to formal GP objects upon funding.

---

## 7.8 Governance UI / UX
To maximize legitimacy and accessibility:

- GitHub issue templates = proposal forms  
- Bounty ledger = real-time transparency (reward, status, TxID)  
- VS-based Cred Scores = optional contributor weights  
- Governance dashboard = proposal timeline + fund-flow visualization  

Wallet integrations will enable direct on-chain voting from proposal pages post-MVP.

---

## 7.9 Economic Safeguards
To protect against capture and abuse:

- **Proposal bonds** discourage spam  
- **Streaming / vested disbursement** for large payouts  
- **Slashing** for fraudulent claims  
- **Idle decay** for unspent allocations  
- **Audit logs** cryptographically linked between GitHub, Sheets, and chain  

These measures embed economic discipline directly into protocol law.

---

## 7.10 Summary
Governance in VeriSphere is **programmable coordination**, not bureaucracy.  
By encoding proposals as GitHub issues, funding them through an exponential reward curve, and executing them via on-chain transactions, VeriSphere unites:

- Decentralized labor markets  
- Transparent project management  
- Mathematically predictable rewards  

Every completed task represents both a **truthful contribution** and a **governance event**, verifiable on-chain and immutable in history.

---

**Summary:**  
The Governance Lane enables verifiable, time-bounded, executable decision-making without contaminating the perpetual truth-staking market.  
KC discovers truth; GP steers the protocol.  
Both use VSP, both are transparent — but only GP finalizes and executes.

---

## 8. Architecture

| Layer | Components | Notes |
|---|---|---|
Core Protocol | Claims, stakes, VS logic, relations, oracle, mint/burn | On-chain |
Indexing | Claim graph, link graph, VS derivations, cross-query | Off-chain indexers |
API | Query, submit claim, stake, link | Open to all |
Clients | Official UI + 3rd-party interfaces | Permissionless |
AI Assist (optional) | Natural-language query + surfacing | Off-chain module |

**On-chain = rules + economics**  
**Off-chain = convenience + discovery**

---

## 9. UI & Data Layer Separation

- Protocol = independent, composable, permissionless
- UI = one of many possible front-ends  
- API supports 3rd-party apps, bots, analytics tools

Users should be able to build:  
- Desktop clients  
- Mobile wallets  
- AI truth-check assistants  
- Research tools  
- Anonymous CLI tools  

VeriSphere = **public truth engine + economic layer**

---

## 10. Roadmap

| Phase | Deliverables |
|---|---|
Alpha | Core contracts, staking engine |
Beta | Graph indexing, governance |
Launch | Public UI, API docs, bounty system |
Scale | AI integration, cross-chain read-oracles |

---

## 11. Conclusion

VeriSphere exposes truth to the ultimate filter: **skin in the game**.

False ideas cost money.  
Correct ideas survive, earn, and rise.  

A global market for truth — open, adversarial, economically honest.

**Put your money where your mouth is.**  
Truth wins when belief has consequence.

---
