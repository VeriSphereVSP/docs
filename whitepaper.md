# VeriSphere: The Game of Staked Truth — A Decentralized Knowledge Market

**Version:** 11.1  
**Date:** October 30, 2025  
**Authors:** VeriSphere Development Team  
**Contact:** info@verisphere.co

---

## Abstract

VeriSphere is a decentralized knowledge-staking protocol that turns truth discovery into a competitive economic game. Users make claims, challenge claims, and **stake VSP tokens** to signal confidence — earning when they align with consensus and burning when they don’t. In short: **put your money where your mouth is**.

Unlike content platforms that rely on moderators or opaque algorithms, VeriSphere is driven by open incentives and transparent math. Every assertion is a post; every agreement or challenge is backed by stake; and evidence can be linked between posts with contextual staking to strengthen or weaken claims. Accurate, well-supported ideas gain visibility and earn rewards. Weak or false claims lose stake and fade.

All protocol fees (e.g., the posting fee) are **pegged to a fixed weight of gold**, not USD. At launch, the posting fee equals the value of **~1/4000 oz. of gold** (≈ $1 at that time), and remains that same gold weight thereafter, regardless of VSP’s market price.

Governance operates inside the same mechanism — protocol upgrades, parameters, bounties, and payments are proposed and decided by staking behavior, not foundation decree.

---

## 1. Purpose & Motivation

- **Problem:** Information systems reward volume and virality, not accuracy.  
- **Approach:** Convert claims into **stakeable propositions** with explicit economic outcomes.  
- **Goal:** A market for truth where signal (accuracy under challenge) outcompetes noise.

---

## 2. Roles & Objects

- **Post (Claim/Assertion):** A single, verifiable statement.  
- **Stake:** VSP locked **for** or **against** a post (or link) to express confidence.  
- **Relation (Link):** A directed edge from a source post to a target post, typed as **support** or **challenge**.  
- **Contextual Staking:** Additional stake placed **on the link within a specific context** (the target thread).  
- **Verity Score (VS):** A post’s confidence metric derived from stake and linked evidence.

---

## 3. Economic Primitives & Fees (Gold-Peg)

- **Posting fee:** Burned; pegged to a fixed weight of gold (e.g., ~1/4000 oz at launch).  
- **Fee memory:** The posting fee is “remembered” and **counts toward the post’s total stake only after the post accumulates ≥ fee in external stake** (either for or against). Until then, the post’s VS remains neutral.  
- **Unstaked decay:** **Unstaked balances burn at the minimum rate** to discourage passive hoarding and encourage participation.  
- **On-chain vs. off-chain pricing:** The oracle provides the gold price; the protocol converts the gold-pegged fee into VSP at execution time.

---

## 4. Verity Score & Relation Mechanics (No Dampening)

### 4.1 Base Verity Score (per post)
Let **Up** be stake supporting the post and **Down** be stake challenging it.  
<code>BaseVS(B) = (2 * Up / (Up + Down) - 1) * 100</code> &nbsp; (clamped to [-100, +100]).

Normalized to 0..1 for weighting:  
<code>nVS(X) = (BaseVS(X) + 100) / 200</code>.

**Activation rule:** <code>BaseVS</code> is treated as **0** until the post’s **external stake ≥ posting fee** (the burned fee is “remembered” only after that threshold).

### 4.2 Relations (links) and types
A **Relation** is a directed edge <code>R: S → A</code> with type <code>t ∈ {+1 (support), -1 (challenge)}</code>.  
- **Standalone link votes**: votes on the link as an independent post (for auditability).  
- **Contextual link stake**: stake placed on the link **within** a specific target context (thread of A).

### 4.3 Link influence on a context
Each link contributes influence to the target proportional to **(i)** the credibility of its source post and **(ii)** the stake on that link in the current context, signed by its type.

- **Source credibility:**  
  <code>Cred(S) = nVS(S)</code>.

- **Contextual stake on link R:**  
  <code>StakeOnLink<sub>R,A</sub></code> (stake staked on R **in the context of A**).

- **Per-link influence on A:**  
  <code>Influence<sub>R→A</sub> = α * Cred(S) * StakeOnLink<sub>R,A</sub> * t</code>, where <code>α &gt; 0</code> is a governed scaling factor mapping stake units to VS points.

- **Derived Verity Score of A (with links):**  
  <code>DerivedVS(A) = clamp( BaseVS(A) + Σ<sub>R: *→A</sub> Influence<sub>R→A</sub>, -100, +100 )</code>.

**Notes:**  
- A link is **itself** a post that can be up/downvoted outside any single context; those votes inform its standalone visibility/audit trail, but **only the contextual stake** enters the influence formula above.  
- **Circularity is prohibited:** links that (directly or indirectly) create cycles are rejected at validation.

---

## 5. Staking Dynamics, Yields & Burns

- **Rate band (governed, defined at launch):**  
  - **Maximum staking yield:** <code>10 ×</code> the **US 10-Year Treasury Note** rate (10YUST).  
  - **Minimum staking yield / burn:** <code>0.1 ×</code> 10YUST.  
- **Unstaked decay:** Unstaked balances decay at the **minimum rate**.  
- **Aligned vs. misaligned:**  
  - Aligned stake (with positive <code>DerivedVS</code>) mints at the governed rate.  
  - Misaligned stake burns at the governed rate.  
- **Adversarial participation multiplier (anti-isolation):**  
  Uncontested or trivially isolated posts earn **negligible or zero** staking yield. Yield scales up with meaningful opposing stake (parameterized multiplier, governed).  
- **Reallocation:** Stake can be moved at will (subject to standard lock/settlement rules) to adapt to new evidence.

---

## 6. Visibility & Discovery

- **Visibility score:**  
  <code>Visibility(A) = TotalStake(A) * (DerivedVS(A) + 100) / 200</code>.  
  High-stake, high-verity posts rank higher; low-stake or controversial posts are visible but lower in default views.

- **Atomic incentive rule:**  
  The protocol does not police wording length. However, **any participant may isolate and challenge a single assertion** embedded in a multi-assertion post. Because isolated challenges dilute the original post’s defense efficiency, **rational players publish atomic (single-assertion) posts**.

---

## 7. Game Integrity & Anti-Exploitation

**Threat:** Isolated inflation loops (self-posting and self-staking without engagement).  
**Mitigations built in:**
1. **Posting fee (gold-pegged) burned** — real cost to spam.  
2. **Activation threshold** — VS remains neutral until external stake ≥ fee.  
3. **Unstaked burn** — passive hoarding is penalized.  
4. **Adversarial multiplier** — **negligible/zero yield** if no meaningful opposing stake.  
5. **Challenge incentives** — others profit by challenging weak posts, making isolation negative-EV.

**Outcome:** Profit requires surviving **contest**, not merely posting in isolation.

---

## 8. Governance Inside the Game

- **Mechanism:** Governance proposals are posts; approving or rejecting them is done by staking **for** or **against**.  
- **Scope:** Protocol parameters (e.g., <code>α</code>, rate band, activation thresholds), oracle/collation policies, fee weight, integration changes, treasury rules.  
- **Bounties & Payments:** Work items are posted as bounty proposals; acceptance and payout are triggered by on-chain governance outcomes.  
- **Safeguards (bootstrapping phase):** Minimal guardian controls (pause/rollback) with a predefined sunset via governance to avoid ossification.  
- **Norm:** “Those confident enough to stake are those qualified to decide.”

---

## 9. Architecture: Core vs. Interface

### 9.1 Core Protocol (Public API)
**On-chain (Solana):**
- Posts, links, stake positions, VS state roots, governance proposals, bounty state, fee logic (gold-peg via oracle), circularity checks.

**Off-chain (but protocol-critical) services:**
- Oracle adapters (gold pricing, 10YUST), indexers, proof generators (if used for rollups/accumulators).  
- Public **Core API** (gRPC/REST) exposing read endpoints (graph, scores, histories) and transaction builders.

**Guarantees:** Deterministic state, verifiable transitions, public data accessibility.

### 9.2 Interface Layer (Independent Clients)
- Web app(s), mobile apps, CLI, research tools.  
- AI collation, summarization, and UX guidance live **outside** the core and consume the **Core API**.  
- Third parties can build their own clients; no dependency coupling to the official UI.

---

## 10. On-Chain vs. Off-Chain Data

- **On-chain:** Identifiers, hashes, stake amounts, VS values/roots, relations, governance metadata, fee execution, payouts.  
- **Off-chain:** Full text bodies, AI features, analytics, large attachments, mirrors/cache layers.  
- **Integrity:** Off-chain content is referenced by on-chain hashes; clients verify integrity before display.

---

## 11. Security, Safety & Constraints

- **Cycle rejection:** Any relation that would create a cycle is rejected.  
- **Reorg/latency handling:** Clients display provisional VS until finalization depth.  
- **Sybil resistance:** Economic skin-in-the-game plus adversarial multiplier; optional allowlists or reputation modules are pluggable without changing core math.  
- **Upgradability:** Governance-gated program upgrades; migration plans published as proposals with rollback windows.

---

## 12. Launch Parameters (Governed, Editable Later)

- Posting fee: fixed **gold weight** (~1/4000 oz at launch).  
- Rate band: **max = 10 × 10YUST**, **min = 0.1 × 10YUST**.  
- Scaling factor: <code>α</code> > 0 (initial value set conservatively).  
- Adversarial multiplier: default yields **0** if opposing stake &lt; threshold; scales to 1 as contest deepens.  
- Unstaked burn: enabled at **minimum rate**.

---

## 13. Roadmap

- **Q4 2025:** Core contracts (posts, stake, links, governance), indexer, oracle bridge, public read API.  
- **Q1 2026:** Core open beta; bounty-driven development; third-party client docs.  
- **Q2 2026:** First-party UI/AI client launch; integrations and ecosystem incentives.

---

## 14. License & Attribution

Open-source under a permissive license (to be finalized by governance).  
© 2025 VeriSphere Development Team.
