# VeriSphere Technical Architecture

## 1. Purpose

This document defines the technical architecture for VeriSphere — a decentralized truth-staking protocol where users publish claims, stake to support or challenge them, and link evidence between claims to influence global verity.

The goal is to clearly separate:

- **Core on-chain protocol**
- **Off-chain verity compute engine**
- **Public API layer**
- **Client applications (first-party and third-party)**

This serves as a development specification.

---

## 2. High-Level System Architecture

| Layer | Function |
|---|---|
On-Chain Protocol | Immutable registry, stake accounting, mint/burn, governance |
Off-Chain Verity Engine | Computes Verity Scores & link propagation (deterministic algorithm) |
Storage & Indexing | IPFS/Arweave + database for content, stakes, and graph traversal |
Public API | Read/write interface for apps, bots, UIs, research tools |
Clients | Website, SDKs, CLI, third-party apps |

---

## 3. Core Data Model

### 3.1 Post (Claim)

A **Post** is a single textual assertion.

Fields:
- post_id (hash)
- author_wallet
- timestamp
- content_uri (IPFS/Arweave)
- optional context metadata (original thread)

Rules:
- Must be **one assertion only**
- Additional arguments → separate posts linked contextually
- Posting fee is **gold-pegged and burned**
- Posting fee does not count toward Verity Score until ≥ posting fee stake exists on either side

### 3.2 Stake

Stakes represent belief:

- support stake (agree)
- challenge stake (disagree)

Users may:
- add stake
- remove stake
- flip stake side

Unstaked VSP **decays at the minimum rate** to discourage passive ambush opportunism.

### 3.3 Relation

A **Relation** links Post B → Post A with direction and type:

- support (B reinforces A)
- challenge (B undermines A)

Relations carry contextual stake: users may vote on correctness of the relation itself.

### 3.4 Governance Proposal

Governance uses the same staking mechanics — proposals are claims, staking = voting.

---

## 4. Verity Score System

### 4.1 Base Verity Score (direct votes only)

BaseVS = (2 * (Agree / Total) - 1) * 100
Range = [-100, +100]

makefile
Copy code

Normalized:

nVS = (BaseVS + 100) / 200
Range = [0,1]

nginx
Copy code

### 4.2 Link Influence

A linked post’s influence on a context post:

Influence = nVS(linkPost) * stake_on_link_in_context

yaml
Copy code

Aggregate link influence modifies the context post's verity while **never overriding direct stake**.

Circular references prohibited.

---

## 5. Token & Incentive System

### 5.1 VSP Token

- Elastic supply
- Mint on aligned stakes
- Burn on misaligned stakes
- Unstaked balance burns at minimum rate

### 5.2 Posting Fee

- Gold-pegged (launch reference: ~1/4000 oz ≈ 1 VSP)
- Burned
- Incentivizes concise assertions
- Prevents spam

### 5.3 Reward Curve (launch parameters, governance-controlled)

| Condition | Rate |
|---|---|
Smallest stake pools | 10× US 10-year Treasury rate |
Largest stake pools | 1/10× US 10-year Treasury rate |
Unstaked balances | Burn at minimum rate |

Rationale:
- Incentivizes early discovery of truth
- Limits reward farming via large pools
- Discourages passive whales

---

## 6. On-Chain Contract Suite

| Contract | Function |
|---|---|
Post Registry | Registers claim hashes |
Stake Contract | Stake add/remove/flip, accounting & burns/mints |
Relation Registry | Registers directed evidence links |
Token Contract | VSP mint/burn |
Governance Contract | Parameter changes triggered by staked consensus |
State Root Anchor | Stores Merkle commitments from verity engine |

Only **proof-relevant primitives** live on-chain.

---

## 7. Off-Chain Verity Engine

Deterministic compute pipeline:

- Ingests on-chain events
- Computes:
  - Base verity
  - Relation propagation
  - Time-based reward curves
  - Merkle state snapshots
- Publishes:
  - Updated verity states
  - Graph traversal data
  - API-ready indexed content

Future: ZK proofs for verity computations.

---

## 8. Storage & Indexing

| Storage | Contents |
|---|---|
IPFS/Arweave | Post text & metadata |
Database | Post graph, stake events, relation context, event logs |
Search Index | Full-text + semantics |
Cache | Trending, hot disputes, high-signal claims |

Posts remain readable even if UI is offline.

---

## 9. Public API

### Access Methods

- HTTPS REST
- WebSockets (live stakes & verity updates)
- SDKs (JS/TS first; others later)

### Core Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
POST | /post | Submit claim |
POST | /stake | Add/remove/flip stake |
POST | /relation | Link claims |
GET | /post/{id} | Fetch claim |
GET | /score/{id} | Verity data |
GET | /graph/{id} | Argument graph |
GET | /feed/trending | Highest signal claims |
GET | /governance/proposals | View proposals |

Auth = crypto wallet signature

---

## 10. Client Layer

### Official Client (verisphere.co)
- Claim browser
- Stake interface
- Graph viewer
- Wallet connect
- AI-assisted retrieval & argument mapping

### Third-Party Clients
- Wallet integrations
- Research UIs
- Journalism tools
- Fact-checking extensions
- Automated disputation bots

Goal: **ecosystem, not app**

---

## 11. Governance

- All rules can be changed by staked governance
- Governance proposals are **claims inside the system**
- Staked consensus triggers contract actions
- Treasury used for development grants & bounties

Meta-rule: **Put your money where your mouth is — even in governance**

---

## 12. Security & Attack Resistance

| Attack | Mitigation |
|---|---|
Spam claims | Gold-pegged posting fee (burn) |
Whale ambush | Unstaked decay + slashing risk |
Long essay claims | Fee proportional to length |
Echo chambers | Counter-stake exposure + network linking |
Sybil identities | Wallet cost + stake accountability |
Propaganda capital floods | Economic loss on wrong claims |
Token hoarding | Minimum burn rate |

In VeriSphere, **bad actors lose money — not attention**.

---

## 13. Roadmap

| Phase | Deliverables |
|---|---|
Phase 1 | Contracts, CLI, verity engine prototype |
Phase 2 | API + explorer |
Phase 3 | Official UI, wallet UX, AI navigation |
Phase 4 | ZK verity proofs, federated deployments |

---

## 14. Design Principles

- No moderators — only economics
- No reputation scores — only truth pressure
- Every claim challengeable
- Precision rewarded, ambiguity punished
- Open composability — anyone can build clients
- Truth emerges by survival, not authority

---

## 15. Summary

VeriSphere is an economic truth-discovery engine.

- On-chain: incentives, stake, governance
- Off-chain: verity compute, graph logic, indexing
- Open API → any app can access the truth market
- Only risk-bearing assertions matter
- Disinformation costs money  
Real belief earns.

A market for truth — not trust.
