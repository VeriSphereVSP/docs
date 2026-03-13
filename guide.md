# How to Play VeriSphere

## What is VeriSphere?

VeriSphere is a truth-staking game where you back factual claims with real VSP tokens. If you're right, you earn. If you're wrong, you lose. The community decides what's credible through economic consensus — not votes, not likes, not algorithms.

---

## Getting Started

### 1. Connect Your Wallet
Click **Connect Wallet** in the top right. You'll need MetaMask (or a compatible wallet) on the **Avalanche Fuji Testnet**. You don't need any AVAX for gas — VeriSphere pays all transaction fees for you.

### 2. Get VSP Tokens
Click **Buy** in the wallet bar to purchase VSP with USDC. VSP is the only token you need to play. You can sell VSP back at any time.

### 3. Explore a Topic
Type any topic in the search bar — "climate change", "earth", "quantum computing" — and VeriSphere generates an article with factual claims. Each claim can be staked, challenged, and linked to evidence.

---

## The Game

### Claims
A **claim** is a factual assertion, like "Earth is a spheroid" or "The greenhouse effect is caused by atmospheric gases." Claims live on-chain forever. Creating a claim costs **1 VSP** (burned as a fee) plus an initial stake.

### Staking
Every claim has two sides: **support** and **challenge**.

- **Positive number** (+1, +5, etc.) = stake in **support** (you believe the claim is true)
- **Negative number** (-1, -5, etc.) = stake in **challenge** (you believe the claim is false)

Your stake earns or loses value over time based on the claim's **Verity Score (VS)**.

### Verity Score (VS)
The VS reflects economic consensus:

- **VS > 0%** → More support than challenge. Supporters earn, challengers lose.
- **VS < 0%** → More challenge than support. Challengers earn, supporters lose.
- **VS = 0%** → Contested or inactive. Nobody earns or loses.

The VS is shown as a colored number: green for positive, red for negative.

### Evidence Links
Claims don't exist in isolation. You can link one claim to another as **support** or **challenge**:

- "Earth is a spheroid" **challenges** "Earth is flat" → If the challenger is credible (VS > 0), it pushes the target's VS down.
- "CO2 absorbs infrared" **supports** "Greenhouse effect is real" → Credible support pushes the target's VS up.

Links are also stakeable. Staking on a link means "I believe this evidence relationship is valid."

**Key rule: Only credible claims influence others.** If a claim's VS drops to zero or below, all its outgoing links go silent — it can't affect other claims until it's rehabilitated with direct support.

---

## How to Win

### Strategy 1: Back the Truth Early
Find claims that are true but undervalued. Stake support early — you get the best queue position, which means the highest earning rate. As more people agree and stake support, the VS rises, and your position earns faster.

### Strategy 2: Challenge Misinformation
Find claims that are false but have support. Stake challenge. If you're right and the community follows, the VS goes negative, and challengers earn while supporters lose their stake.

### Strategy 3: Build Evidence
Instead of staking directly on a crowded claim, create or stake on **evidence links**. A well-staked challenge link from a credible source can flip a claim's VS negative — and your link stake earns from a smaller, less competitive pool.

### Strategy 4: Defend Your Positions
If someone challenges a claim you support, you can:
- Add more direct support stake
- Challenge the challenger's claim (reduce its VS, reduce its influence)
- Challenge the evidence link itself (silence it)

---

## Earning Rate (APR)

Your earning rate depends on four factors:

1. **Truth Pressure (v)** — How strong the VS is. |VS| = 100% means maximum pressure. VS = 0% means no earnings.
2. **Post Size (p)** — Larger stakes face stronger pressure. Your post's total stake divided by the system-wide maximum.
3. **Queue Position** — Earlier stakers earn more. The queue is divided into tranches; tranche 1 earns up to 10× more than tranche 10.
4. **Rate Bounds** — Minimum 1% APR, maximum 100% APR (governance-configurable).

**Formula:** `APR = (r_min + (r_max - r_min) × v × p) × queue_weight`

Winners (side aligned with VS) earn at this rate. Losers (opposing side) lose at this rate.

---

## Key Concepts

### Posting Fee
Creating a claim or link costs **1 VSP**, which is permanently burned. This prevents spam.

### Activity Threshold
A claim needs at least 1 VSP total stake to be "active" and influence other claims through links.

### Credibility Gate
Only claims with VS > 0 can influence other claims through evidence links. A discredited claim (VS ≤ 0) is inert in the evidence graph until rehabilitated.

### Conservation of Influence
A claim's influence is distributed — not duplicated — across its outgoing links. Creating more links from the same claim dilutes each link's share.

---

## Quick Reference

| Action | Cost | What it does |
|--------|------|-------------|
| Create claim | 1 VSP fee + initial stake | Publishes a factual assertion on-chain |
| Create link | 1 VSP fee + initial stake | Connects two claims as support or challenge |
| Stake support | Any amount | Backs a claim as true (earns if VS > 0) |
| Stake challenge | Any amount | Backs a claim as false (earns if VS < 0) |
| Withdraw | Free | Removes your stake at any time |
| Buy VSP | USDC | Purchase tokens to play |
| Sell VSP | Free | Convert tokens back to USDC |

---

## Tips

- **Start small.** Stake 1 VSP to learn how the system works before committing more.
- **Check the evidence graph.** A claim might look safe but have a strong incoming challenge link that's about to flip its VS.
- **Queue position matters.** Being first to stake on a new claim gives you the best earning rate.
- **Links are cheaper plays.** Staking on a link lets you influence a claim's VS without competing in a large direct stake pool.
- **Watch the Portfolio.** Your Portfolio page shows real-time APR, position status, and the factors behind your earnings.
- **VS = 0 is not safe.** A claim with VS = 0 isn't earning anything, and one well-funded challenge can push it negative quickly.
