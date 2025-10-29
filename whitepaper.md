# VeriSphere: The Game of Staked Truth – A Decentralized Knowledge Market

**White Paper**  
Version 11.0  
Date: October 29, 2025  
Authors: VeriSphere Development Team  
Contact: info@verisphere.co  

---

## 1. Abstract

VeriSphere transforms knowledge verification into a decentralized prediction game. Users stake **VSP tokens** on claims, forming a dynamic **market of truth**. Aligning with consensus earns rewards; opposing it risks losses. The platform combines the community wisdom of Wikipedia, Quora, and Reddit with blockchain-based validation, allowing posts to be modified or overridden based on staked consensus.  

Each post’s **Verity Score (VS)** represents staked agreement vs. disagreement, continuously updated as stakes change. Relations between posts (supports, conflicts) propagate influence across the network. VSP mints and burns dynamically, rewarding early and accurate participation. Fees like the 1 VSP posting cost are pegged to $1 (based on gold value), ensuring accessibility. VeriSphere gamifies truth-seeking—turning verification into a competitive, self-sustaining market.

---

## 2. Introduction

The digital information ecosystem faces a credibility crisis. Traditional platforms (Wikipedia, Quora, StackExchange) rely on moderation and reputation systems—susceptible to bias and groupthink. Prediction markets like Polymarket incentivize correctness but are limited to discrete, one-time events.

**VeriSphere** unites these concepts into a **continuous, decentralized knowledge market**. Users post assertions, stake to agree or disagree, and influence evolving Verity Scores that represent community consensus.  

- **Incentivized truth-seeking:** Users profit for aligning with accurate consensus.  
- **Unified knowledge graph:** Integrates curated sources with staked user input.  
- **Dynamic adaptation:** Scores evolve as evidence and stakes shift.  
- **Self-balancing tokenomics:** Minting and burning maintain equilibrium.  

Governance is decentralized, allowing VSP holders to propose and vote on protocol changes.

---

## 3. Problem Statement

### 3.1 Misinformation Persistence  
False information thrives because it’s free to spread. VeriSphere introduces **economic friction**—false or unpopular stakes lose VSP, deterring low-effort or deceptive content.

### 3.2 Lack of Incentives  
Contributors to existing platforms aren’t rewarded for accuracy. VeriSphere directly links economic outcomes to verity alignment.

### 3.3 Fragmented Knowledge  
Knowledge is siloed across multiple platforms. VeriSphere merges these sources and overlays them with staked consensus for unified insight.

### 3.4 Static Systems  
Traditional sites fail to adapt as understanding evolves. VeriSphere’s **perpetual staking model** ensures real-time updates to all claims.

### 3.5 Prediction Market Limitations  
Existing markets resolve single outcomes; VeriSphere supports **ongoing debates**, reflecting evolving consensus on non-binary or continuous topics.

---

## 4. VeriSphere Overview

- **Searchable Knowledge Graph:** Indexed posts ranked by Verity Score.  
- **Threaded Relations:** Posts linked as supports or conflicts.  
- **Continuous Updates:** Scores and rewards evolve dynamically.  
- **AI Integration:** External data from Wikipedia, Reddit, and others is collated and modified based on stake-weighted truth values.  
- **Prediction Market Mechanics:** Users can speculate or invest in ongoing knowledge debates.  
- **Dynamic Token Incentives:** Mint/burn mechanisms scale with stake and accuracy.  

---

## 5. User Interface and Visibility Mechanics

**Visibility Algorithm:**  
Each post’s visibility score = **total_stake × normalized Verity Score**, ensuring that posts with both high engagement and accuracy rise to prominence.

**Key UI Elements:**  
- Post cards with Verity meters and stake charts.  
- Relation graphs (supports/conflicts) visualized via D3.js.  
- Staking and prediction prompts.  
- Chat-style query interface for asking questions directly.

**Principles:**  
- No arbitrary moderation—visibility purely stake-based.  
- All posts accessible, though low-verity ones are ranked lower.  
- Merit-based discovery fosters transparency and engagement.  

---

## 6. Game Mechanics and Logic

### 6.1 Posting
Users can post any claim or response. Posting incurs a **1 VSP fee**, dynamically pegged to $1 (based on gold oracle). The fee discourages spam and is burned immediately but still counts as initial stake.

### 6.2 Staking and Interest
- **Agree/Disagree Stakes:** Users stake to support or oppose a post.  
- **Variable Interest:** Minted VSP rewards proportional to alignment with eventual consensus.  
- **Inverse Reward Curve:** Higher rewards for early or low-stake participation.  
- **Penalty for Inactivity:** Unstaked VSP loses value at a minimal rate.

At launch:
- Maximum rate = 10× US10Y (U.S. 10-Year Treasury yield).  
- Minimum rate = 1/10× US10Y.  
Rates adjust via governance.

### 6.3 Post Updates and Versions
- Posts are **immutable**; new versions are linked as descendants.  
- Users may **migrate stakes** to newer posts.  
- No deletions—immutability ensures transparency.

---

## 7. Verity Score and Relation Mechanics

### 7.1 Core Verity Score Formula
\[
VS = (2 \times \frac{agree\_stake}{total\_stake} - 1) \times 100
\]
Example:  
10 VSP agree, 5 VSP disagree → \(VS = (2×10/15 - 1)×100 = 33.3\)

### 7.2 Relations and Influence Flow
Posts can **support** or **conflict** with others. A link between posts transmits influence proportionally to both the **Verity Score** and **stake intensity** of the linked post.

Each link has:
- Independent Verity Score (from its own votes).
- Contextual votes (up/down) specific to the post it’s linked to.

**Influence Formula:**  
\[
VS_{context} = \frac{(agree_{context} \pm \sum(link_{VSnorm} \times link\_votes))}{(total_{context} + \sum(link\_total))} \times 100
\]
where  
\(link_{VSnorm} = (link_{VS} + 100) / 200\)

Supports add; conflicts subtract.  
Circular references are **prohibited**.  

### 7.3 Aggregate Link Behavior
- Each post’s **total Verity Score** = native votes + aggregate of contextual link votes.  
- Each link affects all contexts it’s used in, weighted by its own Verity Score.  
- Influence decays logarithmically with network distance to prevent runaway amplification.

## Diagram — Relation and Influence Flow

```mermaid
graph TD
    subgraph ContextA["Context: Post A (VS=30)"]
        A["Post A"]
    end
    subgraph Supports
        L1["Post L1 (VS=80) Supports A"]
        L2["Post L2 (VS=-50) Supports A"]
    end
    subgraph Conflicts
        L3["Post L3 (VS=60) Challenges A"]
    end
    L1 -->|"Support (+)"| A
    L2 -->|"Support (+)"| A
    L3 -->|"Conflict (-)"| A
    classDef support fill:#a3e4d7,stroke:#1abc9c,stroke-width:2px,color:#000;
    classDef conflict fill:#f5b7b1,stroke:#c0392b,stroke-width:2px,color:#000;
    classDef context fill:#aed6f1,stroke:#2471a3,stroke-width:2px,color:#000;
    class A context;
    class L1,L2 support;
    class L3 conflict;

---

## 8. AI Integration and Knowledge Collation

### Workflow
1. **User Query:** Input question (e.g., “Is nuclear power sustainable?”).  
2. **Internal Search:** Finds matching staked posts.  
3. **External Augmentation:** If insufficient, pull from Wikipedia, Quora, Reddit, etc.  
4. **Stake Overlay:** Modify factual responses with staked corrections.  
5. **Interactive Output:**  
   Example:  
   > Wikipedia says X, but VeriSphere consensus (1,200 VSP agree, 200 disagree) corrects it to Y.

The AI is fine-tuned for **consensus aggregation** rather than opinion generation.

---

## 9. Tokenomics

- **Token Name:** VeriSphere Token (VSP)  
- **Supply:** Uncapped, dynamically minted/burned.  
- **Initial Price:** 1 VSP ≈ $1 (launch peg).  
- **Posting Fee:** Pegged to $1 via gold oracle.  
- **Minting:** Aligned stakes earn new VSP at dynamic rates.  
- **Burning:** Misaligned stakes lose VSP.  
- **Governance:** Each VSP = 1 vote. Protocol updates and reward curves governed on-chain.

**Dynamic Equilibrium:**  
Minting and burning stabilize token value. Low total staking → higher minting incentives; high staking → reduced rates.

---

## 10. Development and Bounty System

VeriSphere is open-source at **[github.com/VeriSphereVSP](https://github.com/VeriSphereVSP)**.  
All development is bounty-based and transparent, using VSP as payment.

**Bounty Model:**
\[
p(n) = 100 + \frac{500,000}{n} \text{ VSP/hour}
\]
- Early contributions earn the most.  
- Rewards asymptotically approach 100 VSP/hour.  
- Paid directly from treasury via verified PRs.  

**Completed Tasks:**  
Whitepaper, Technical Architecture, Domain Setup, GitHub Repos.

**Bounty Categories:**  
- Smart Contracts  
- Frontend UI  
- AI Integration  
- Tokenomics Simulation  
- Governance & DAO Mechanics  

---

## 11. Roadmap

| Phase | Timeline | Milestone |
|-------|-----------|-----------|
| **Q4 2025** | Prototype | Core staking contracts, Verity logic |
| **Q1 2026** | AI Launch | AI-assisted knowledge curation |
| **Q2 2026** | MVP | Full dApp release with staking and prediction mechanics |
| **Q3 2026** | Governance | DAO and treasury activation |
| **Q4 2026** | Expansion | API and cross-market integrations |
| **2027+** | Scale | L2 migration, mobile app, decentralized storage |

---

## 12. Governance and Community

- **DAO Governance:** Each VSP = 1 vote.  
- **Proposal Flow:**  
  1. Create proposal → stake ≥ 1,000 VSP.  
  2. 7-day discussion phase.  
  3. On-chain vote → requires quorum ≥ 5%.  
- **Treasury:** Funds development and rewards through dynamic VSP issuance.  
- **Transparency:** All bounty transactions logged publicly.

---

## 13. Security and Anti-Manipulation

- **Circular References Blocked:** Prevent self-support loops.  
- **Stake Decay:** Idle stakes lose small value to discourage spam.  
- **Identity Neutral:** Wallet-based accounts, optional DID integration.  
- **Audit Trail:** Immutable blockchain record for all edits and stakes.  
- **AI Anomaly Detection:** Identifies suspicious voting or stake bot patterns.

---

## 14. Future Work

- **Cross-chain staking and bridging (ETH, SOL, SVM).**  
- **Integration with decentralized storage (Arweave, IPFS).**  
- **Advanced relation analytics (network topology of truth).**  
- **AI prediction synthesis—dynamic truth forecasting.**  

---

## 15. Conclusion

VeriSphere transforms the internet’s information economy into a **truth economy**.  
By merging staking mechanics, prediction markets, and AI-assisted consensus, it rewards accurate knowledge and penalizes misinformation—without central authority.  

**The game of truth is open. The stakes are real.**  

**Website:** [verisphere.co](https://verisphere.co)  
**Repository:** [github.com/VeriSphereVSP/core](https://github.com/VeriSphereVSP/core)
