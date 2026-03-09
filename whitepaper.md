# VeriSphere: A Truth-Staking Protocol
### White Paper — v14.0
**Date:** March 2026
**Contact:** info@verisphere.co

---

## Abstract

VeriSphere is a decentralized protocol for economically evaluating factual claims. Any participant may publish a claim on-chain and any participant may stake tokens to support or challenge it. Claims accumulate a Verity Score derived from the ratio and magnitude of stakes on each side. Evidence links between claims propagate truth-pressure through a directed graph, creating an interconnected epistemic structure where the credibility of each claim depends on the credibility of its evidence.

The protocol operates on the Avalanche C-Chain using the VSP ERC-20 token. All scoring, staking, and evidence-linking logic is implemented in upgradeable Solidity contracts. The protocol is permissionless: any front-end, API, or automated agent may interact with the on-chain contracts directly.

---

## 1. Motivation

Existing information systems lack a mechanism for attaching economic cost to factual assertions. Search engines rank by engagement. Social platforms rank by virality. Encyclopedias rely on editorial consensus. Prediction markets handle binary, terminal events but cannot evaluate persistent, evolving claims such as "nuclear energy is environmentally sustainable" or "dietary saturated fat increases cardiovascular risk."

VeriSphere addresses this gap by introducing a protocol where:

- Publishing a claim requires burning a fee, eliminating zero-cost spam.
- Supporting or challenging a claim requires staking tokens, imposing a cost on both truthful and untruthful assertions.
- Correct positions accrue value over time; incorrect positions lose it.
- Evidence relationships between claims are first-class on-chain objects with their own stake and credibility.

The protocol does not determine truth. It creates economic pressure that makes being wrong expensive and being right profitable, and it makes the resulting score transparent and auditable.

---

## 2. Protocol Overview

### 2.1 Posts

The atomic unit of the protocol is a **post**. Posts are of two types:

- **Claims**: standalone factual assertions (e.g., "Earth's mean radius is approximately 6,371 kilometers").
- **Links**: directed evidence relationships between two claims, annotated as either support or challenge.

Each post is identified by a sequential post ID. Post IDs begin at 1; zero is reserved as a null sentinel. Posts are immutable once created.

### 2.2 Claims

A claim is a single factual assertion stored as a UTF-8 string on-chain. Claims are deduplicated via case-insensitive, whitespace-normalized hashing (lowercase ASCII, collapse whitespace, trim, then keccak256). Attempting to create a duplicate claim reverts with `DuplicateClaim(existingPostId)`.

Publishing a claim requires transferring a posting fee of 1 VSP to the protocol, which burns it. The fee amount is governance-configurable.

### 2.3 Links

A link is a directed edge from one claim to another, annotated as either **support** or **challenge**. The direction is `from → to`, where "from" is the claim providing evidence and "to" is the claim receiving evidence.

Example: if claim S ("Earth is a spheroid") challenges claim F ("Earth is flat"), the link is `S → F` with `isChallenge = true`. This means S is the evidence provider and F is the evidence receiver.

Links are also posts and carry their own post ID, staking pool, and Verity Score. Duplicate links (same from, to, and challenge flag) are rejected. Self-loops are rejected.

The link graph permits cycles. Two claims may challenge each other simultaneously. The Verity Score computation handles cycles through a stack-based visited-node mechanism (Section 4.3).

Creating a link also requires the posting fee, which is burned.

---

## 3. Staking

### 3.1 Positional Staking

Any participant may stake VSP tokens on any post (claim or link) on either side:

- **Support**: assert the claim is true or the evidence link is credible.
- **Challenge**: assert the claim is false or the evidence link is not credible.

Stakes are recorded in a FIFO queue per side per post. Earlier stakes occupy higher-risk, higher-reward positions. Later stakes occupy lower-risk, lower-reward positions.

Stakes may be withdrawn at any time. Withdrawal from the front of the queue (LIFO) shifts remaining stakes forward into riskier positions.

### 3.2 Staking Rate

Each stake accrues or loses value continuously according to an annualized rate determined by:

1. **Queue position** — earlier stakes face greater exposure.
2. **Post size** — stakes on larger pools face greater pressure.
3. **Truth pressure** — the absolute value of the Verity Score determines the strength of the economic force.
4. **Governed bounds** — rates are bounded between a minimum (1% APR) and maximum (100% APR).

For a stake on the side aligned with the VS sign, value accrues. For a stake on the opposing side, value is burned. The rate formula is:

```
r_i = max(r_min, r_max × (q_i / Q_max) × (p_i / P_max) × (|VS| / 100))
```

Where `q_i` is the queue index, `Q_max` is the maximum queue index across all active posts, `p_i` is the post's same-side total stake, and `P_max` is the maximum post size.

Per time step `Δt` (in years):

```
Δn = n × r_i × Δt × sgn
```

Where `sgn = +1` if the stake's side matches the VS sign, and `sgn = -1` otherwise.

---

## 4. Verity Score

### 4.1 Base Verity Score

The base Verity Score reflects the direct stake ratio on a post.

Let `A` = total support stake, `D` = total challenge stake, `T = A + D`.

```
If A > D:   baseVS = +(A / T) × RAY
If D > A:   baseVS = −(D / T) × RAY
If A = D:   baseVS = 0
If T = 0:   baseVS = 0
```

Where `RAY = 10^18` (fixed-point scaling). The VS is clamped to `[-RAY, +RAY]`, corresponding to the range [-100%, +100%].

A post is considered **active** when its total stake meets or exceeds the posting fee. Inactive posts have no effect on other posts' effective VS.

### 4.2 Effective Verity Score

The effective Verity Score of a claim incorporates evidence from incoming links. For each incoming link to claim C:

1. Compute `parentVS` — the effective VS of the parent claim (the evidence provider). If the parent would create a cycle (see 4.3), use the parent's base VS instead.
2. Compute `linkVS` — the base VS of the link post itself. If the link is a challenge link, negate it.
3. Compute `sumOutgoing` — the total stake across all outgoing links from the parent claim (only links with stake ≥ posting fee).
4. Compute `linkStake` — the total stake on this link post.

The contribution of this link to C's effective VS is:

```
contribution = (linkVS × parentVS / RAY) × (linkStake / sumOutgoing)
```

The effective VS is:

```
effectiveVS(C) = clamp(baseVS(C) + Σ contributions, -RAY, +RAY)
```

This ensures that:
- A well-supported link from a high-VS parent has a strong effect.
- A contested link (low linkVS) or one from a low-VS parent has little effect.
- Challenge links invert the contribution direction.
- The parent's influence is distributed across its outgoing links in proportion to their stake, preventing duplication of influence.

### 4.3 Cycle Handling

The link graph permits cycles. The effective VS computation uses a stack-based cycle detection mechanism:

1. When computing `effectiveVS(C)`, maintain a stack of post IDs currently being computed.
2. Before recursing into a parent, check if it is already on the stack.
3. If so, use the parent's **base VS** (not effective VS) as `parentVS`. This breaks the recursion without truncating legitimate deep chains.
4. A hard depth limit of 32 provides additional safety.

This approach ensures:
- Two mutually challenging claims can coexist.
- Symmetric stakes produce symmetric results regardless of computation order.
- Asymmetric link stakes correctly reflect the economic signal from stakers.

---

## 5. Token Economics

### 5.1 VSP Token

VSP is the native ERC-20 token of the protocol, deployed on Avalanche C-Chain. It has governance-controlled mint and burn functions managed through an Authority contract.

### 5.2 Posting Fee

The posting fee is 1 VSP, burned upon post creation. The fee amount is governance-configurable.

The posting fee serves two purposes:
- Spam prevention: imposes a cost on publishing claims.
- Activity threshold: a post must accumulate total stake ≥ the posting fee to become active and influence other posts.

### 5.3 Economic Properties

- **Deflationary pressure**: posting fees are burned, reducing supply.
- **Inflationary pressure**: correct stakes accrue value (minted by the StakeEngine).
- **Equilibrium**: the balance between creation (burning) and staking (minting) is governed by protocol parameters.

---

## 6. Smart Contract Architecture

All contracts are deployed as UUPS upgradeable proxies behind a governance-controlled Authority.

| Contract | Purpose |
|----------|---------|
| VSPToken | ERC-20 token with Authority-controlled mint and burn |
| PostRegistry | Creates claims and links, burns posting fees, stores post metadata |
| LinkGraph | Stores directed evidence edges, enforces self-loop and duplicate prevention |
| StakeEngine | Manages per-post staking queues, computes positional rates, handles withdrawals |
| ScoreEngine | Computes base and effective Verity Scores with cycle-aware recursion |
| ProtocolViews | Read-only aggregation of claim summaries, edge data, and scores |
| PostingFeePolicy | Governance-configurable posting fee |
| StakeRatePolicy | Governance-configurable staking rate bounds |
| ClaimActivityPolicy | Defines the minimum stake threshold for post activation |
| Authority | Role-based access control (minter, burner, governance roles) |

### 6.1 Meta-Transactions

The protocol supports gasless meta-transactions via an ERC-2771 trusted forwarder (OpenZeppelin `ERC2771Forwarder`). Users sign EIP-712 typed data; a relay submits the transaction on-chain. This allows interaction without requiring users to hold AVAX for gas.

The forwarder is trusted by all governed contracts (PostRegistry, StakeEngine, LinkGraph) through the `ERC2771ContextUpgradeable` base class.

### 6.2 Governance

Governance operates through a `TimelockController` that controls parameter changes, contract upgrades, and treasury operations. During the initial phase, governance is managed by a multisig. The protocol is designed to transition to on-chain governance as the ecosystem matures.

Governance can modify:
- Posting fee amount and gold normalization factor
- Staking rate bounds (min and max APR)
- Activity threshold
- Contract implementations (via UUPS proxy upgrades)
- Authority roles

---

## 7. Design Properties

### 7.1 Permissionless

Any address may create claims, create links, and stake. No registration, reputation, or identity is required. Front-ends, bots, and automated agents interact with the same contracts as human users.

### 7.2 Composable

The protocol exposes all state through standard Solidity view functions. Third-party applications may build on top of the protocol: alternative front-ends, analytics dashboards, AI-powered truth-checking tools, and cross-chain bridges.

### 7.3 Non-Finalizing

Claims never "resolve." The Verity Score is a continuous, live signal that reflects the current state of economic commitment. New evidence, new stakes, and new challenges can shift any claim's score at any time. This makes the protocol suitable for persistent, evolving knowledge — not just terminal predictions.

### 7.4 Adversarial

The protocol is designed for adversarial participants. There is no assumption of good faith. Economic incentives align with truthful behavior: being right is profitable; being wrong is costly. The protocol does not enforce truth — it creates conditions under which truth is economically favored.

---

## 8. Deployment

The protocol is deployed on Avalanche C-Chain (chain ID 43113 for testnet, 43114 for mainnet). Avalanche provides sub-second finality, EVM compatibility, and low transaction costs suitable for interactive staking.

The protocol may optionally be deployed on a dedicated Avalanche Subnet for isolated throughput and custom gas economics.

---

## 9. Conclusion

VeriSphere defines a minimal, permissionless protocol for attaching economic consequence to factual assertions. Claims compete in an open market of support and challenge. Evidence links create a directed graph where credibility propagates through stake-weighted connections. The Verity Score provides a transparent, continuously updated signal of economic consensus.

The protocol does not determine truth. It makes truth economically consequential.
