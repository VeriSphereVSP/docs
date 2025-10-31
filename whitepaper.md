# VeriSphere: A Game of Staked Truth  
### White Paper — v12.0 (Draft)  
**Date:** October 2025  
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

## 7. Governance Lane (“GP” Namespace)

Truth discovery and protocol stewardship must coexist but operate under fundamentally different rules.  
VeriSphere therefore defines two parallel, interoperable lanes:

- **Knowledge Claims (KC):** perpetual, open-ended truth-staking market  
- **Governance Proposals (GP):** time-bounded, executable protocol decisions

KC maintains epistemic integrity (“truth never finalizes”).  
GP provides operational finality (“decisions must finalize”).

### 7.1 Governance Goals

Governance exists to:

- Maintain and evolve core protocol parameters
- Approve upgrades, treasury allocations, and economic changes
- Support community bounties and ecosystem expansion
- Preserve long-term credibility and security

Governance is minimally interventionist; the truth market must remain primary.

### 7.2 GP Proposal Lifecycle

Governance proposals are discrete on-chain objects with a structured lifecycle:

1. **Draft**  
   - Anyone may draft a proposal
   - Simulated feasibility and economic impact recommended

2. **Activation / Voting Window**  
   - Fixed time period (e.g., 5–14 days)
   - **Snapshot voting power** taken at activation to prevent last-minute capital swings

3. **Grace / Timelock**  
   - Delay between approval and execution  
   - Allows vetoes, bug disclosures, or emergency pauses

4. **Execution or Expiry**  
   - Successful proposals **execute automatically on-chain**
   - Failed proposals expire without effect

### 7.3 Voting Power Models

Governance may mix or evolve weighting models; candidate mechanisms include:

- **Staked VSP weight** (primary default — aligns incentives)
- **Unstaked balance component** (optional minority weight)
- **Cred Score multiplier** (performance-based trust derived from KC outcomes)
- **Quadratic modifier** (optional anti-whale component)

Weights are tunable by governance.

### 7.4 Quorum, Thresholds, and Safeguards

Policy parameters set by governance:

- **Quorum requirement**
- **Approval threshold**
- **Turnout guardrails** (min/max to prevent apathy capture)
- **Proposal deposit / bond** (prevents spam; returned if proposal meets quality threshold)

Emergency controls (rare use only):

- **Circuit breaker / guardian delay**
- **Global timelock extension**

### 7.5 Executable Authority

Executed proposals can:

- Modify protocol parameters (fee rates, stake mechanics, caps)
- Manage treasury funds (grants, burns, incentives)
- Authorize upgrades to core contracts and APIs
- Assign or revoke governance roles on upgradeability controllers
- Approve new modules (e.g., L2 bridges, identity oracles)

**All actions are on-chain transactions**, enforceable without off-chain trust.

### 7.6 Interaction With KC Lane

Knowledge staking and governance are related but distinct:

- KC stakes **do not auto-count** in GP unless included in voting formula
- KC outcomes **do not force protocol changes** (truth ≠ enactment)
- GP can modify KC parameters but cannot cherry-pick claim outcomes

This separation preserves epistemic independence and market integrity.

### 7.7 Proposal Types

Common governance proposal classes:

- **Parameter changes** (posting fee factor, yield bands, decay rates)
- **Treasury allocations** (bounties, ecosystem funding)
- **Protocol upgrades** (logic modules, new staking primitives)
- **Foundation actions** (partnership approvals, legal governance)
- **Emergency responses** (halts or mitigations — formalized and auditable)

### 7.8 Governance UI and UX

To maximize legitimacy:

- Proposal templates and on-chain metadata
- Clear impact visualization and code diffs
- Voting guides and simulation tools
- Public audit trails and vote receipts
- Mobile and desktop wallet coverage

### 7.9 Economic Safeguards

To protect against governance capture:

- **Proposal bonds** to discourage frivolous actions
- **Staged treasury access** (streaming, vesting, or capped withdrawals)
- **Slashing or lock-up rules** for malicious governance attempts

Economic resistance complements social consensus and code security.

---

**Summary:**  
The Governance Lane enables verifiable, time-bounded, executable decision-making without contaminating the perpetual truth-staking market.  
KC discovers truth; GP steers the protocol.  
Both use VSP, both are transparent — but only GP finalizes and executes.


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
