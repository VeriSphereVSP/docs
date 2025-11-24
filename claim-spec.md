# claim-spec.md
VeriSphere Claim and Linking Specification (MVP Edition)
Version: 2025-11
Encoding: ASCII-safe UTF-8

1. Overview
-----------
This document defines the on-chain data structures, invariants, and behavioral rules for VeriSphere Claims (Posts). All content is ASCII-safe.

2. Claim Object
---------------
Fields:
- postId
- text
- creator
- createdAt
- postingFeeBurn
- supportTotal
- challengeTotal
- active
- supersedes
- supersededBy

Derived:
- totalStake = supportTotal + challengeTotal
- VS = Verity Score (section 4)

Claims are immutable and atomic.

3. Posting Rules
----------------
Posting fee burned. Claims become active when total stake >= postingFee. No edits allowed.

4. Verity Score
---------------
Let A = support stake, D = challenge stake, T = A + D.

VS = (2 * (A / T) - 1) * 100

If T = 0 or T < posting fee, VS = 0.

5. Evidence Links
-----------------
Fields:
- fromPost
- toPost
- relationType
- ctxStake

Normalized source score:
nVS = (BaseVS + 100) / 200

Support link contribution:
effectiveSupport += nVS * ctxStake

Challenge link contribution:
effectiveChallenge += nVS * ctxStake

Graph must remain acyclic.

6. Staking
----------
StakeLot contains:
- postId
- staker
- amount
- side
- positionIndex
- entryTimestamp
- accruedNet
- withdrawn

Weight:
w_i = (1 / i) / H_N
Where H_N is the harmonic sum 1 + 1/2 + ... + 1/N.

7. Yield and Burn
-----------------
Let:
- n = stake amount
- dt = time (years)
- VS = Verity Score
- v = abs(VS) / 100
- side = support or challenge
- sgn = +1 if aligned with VS, -1 if opposite
- S = total supply
- A = active claims
- T = total stake on claim
- Rmax, Rmin = governed APR bounds

Maturity:
K = S / A
f(T) = T / (T + K)

Effective rate:
r_eff = Rmin + (Rmax - Rmin) * v * f(T)

Stake update:
dn = n * sgn * w_i * r_eff * dt
n_next = max(0, n + dn)

8. Stake Operations
-------------------
Add stake: inserted at tail.
Withdraw stake: removed and settled.
Flip: remove from one side, append to opposite queue.

9. Supersession
---------------
A claim may supersede another. Old claim marked superseded but remains valid for staking.

10. Invariants
--------------
1. Link graph is a DAG.
2. Claims immutable.
3. VS defined for all active claims.
4. Stake never negative.
5. Supply changes only via mint, burn, posting fees.

11. Events
----------
PostCreated
StakeAdded
StakeRemoved
StakeFlipped
LinkCreated
VSUpdated

12. Off-chain Responsibilities
------------------------------
Off-chain systems handle:
- atomicity checks
- duplicate detection
- semantic filtering
- indexing

