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

- Any player may publish a single atomic assertion, called a Post.
- Each Post must contain only one claim.
- Publishing a Post requires a gold-pegged fee (burned).
- A Post begins at Verity Score (VS) = 0 until total stake on the Post (support or challenge) reaches at least the posting fee.
- The posting fee does not earn yield, but does count toward total stake, once additional stake reaches the fee threshold.
- Posts cannot be edited; corrections must be posted as new Posts and linked.

### 3.2 Staking on Claims

Players may stake VSP to either:

- Support a Post (assert it is true), or
- Challenge a Post (assert it is false)

Stake can be:

- Added incrementally
- Withdrawn (with position effects, see below)
- Flipped from support to challenge or vice-versa

Stakes earn or lose value depending on whether they align with the Post's consensus truth, as represented by Verity Score.

### 3.3 Verity Score (VS)

The Verity Score measures consensus belief in a Post:

VS = (2 × (support stake ÷ total stake) − 1) * 100

Range:

- +100 means total belief that the claim is true
- 0 means unclear or split
- −100 means total belief the claim is false

VS continuously updates as stakes change.

### 3.4 Positional Staking System

Stake on each side forms a queue ordered by arrival time.

Principles:

- Earlier stake carries higher risk and higher reward.
- Earlier stake loses more when wrong and earns more when right.
- Later stake earns less and loses less, creating lower-risk entry as claims mature.
- When stake is removed, later stake shifts forward to occupy earlier positions.

This system incentivizes:

- Early honest conviction
- Discouraging opportunistic “wait-and-snipe” behavior
- Allowing corrective flips when falsehoods accumulate stake
- Meaningful capital commitment to defend claims

### 3.5 Reward and Loss Distribution

Rewarding aligned stake:

- A stake earns yield proportional to its position weight, VS magnitude, and total stake magnitude.
- Higher VS and higher total stake means higher trust premium for aligned stake holders.

Penalizing misaligned stake:

- Misaligned stake burns value at the same curve as aligned stake earns.
- Early wrong conviction loses the most, discouraging reckless claims.

If VS = 0:

- Neither side earns or loses, encouraging discovery staking until clarity emerges.

### 3.6 Economic Function

This creates dynamic information markets where:

- Early correct stakers gain the most.
- Early wrong stakers lose the most.
- Late stakers profit modestly but with lower risk.
- Weak claims can be flipped by coordinated challenge capital.
- Strong true claims become economically “fortified”.
- Strong false claims leak value until corrected.

Unstaked balances degrade at the minimum burn rate to discourage passive ambush (holding tokens idle to snipe emerging claims without exposure).

### 3.7 Summary of Effects

This mechanism rewards:

- Truth-seeking
- Early, honest conviction
- Continuous monitoring
- Active argumentation
- Rational participation

And it penalizes:

- Dishonesty
- Reckless assertion
- Passive speculation
- Manipulative capital ambush tactics

The economy remains self-correcting because:

- Capital must take risk to earn reward.
- Claims cannot be dominated by passive money.
- False claims bleed value until corrected.
- Truth earns yield by surviving challenge over time.


**Rates at launch** (governance-changeable):  
- Max return = **10× US 10-Year Treasury**
- Min return = **1/10 × US 10-Year Treasury**

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

## 7. Governance

### 7.1 Inclusive & In-Game
Governance runs **inside the staking game itself**.  
Players stake on governance proposals the same way they stake on truth claims.

### 7.2 Proposal Types
- Change APR bands  
- Update posting fee formula  
- Adjust oracle sources  
- Modify link/tally rules  
- Define cheat-prevention rules  
- Allocate bounties  
- Elect auditors / stewards  

### 7.3 Safeguard Against Sybil / Idle Exploits
The system naturally deters inflationary “post-farm staking” because:  
- Posting fee burns value  
- Unstaked tokens decay  
- Isolated claims without scrutiny have **no reward path**  
- Linking encourages cross-validation  
- Opposition earns by **attacking weak farm claims**

False claims are **economically hunted**.

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
