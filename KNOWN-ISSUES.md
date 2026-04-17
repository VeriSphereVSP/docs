# VeriSphere Known Issues & Future Work

## Gas Concerns (Non-Urgent, Monitor)

### 1. ScoreEngine.effectiveVSRay — Recursive Gas Cost

**Status:** Mitigated. Bounded fan-in implemented.

**Issue:** `effectiveVSRay` recursively calls `getIncoming` and
`getOutgoing` across LinkGraph and StakeEngine, with depth up to 32.
Each level loads dynamic arrays from storage. A claim with many
incoming links from parents that each have many outgoing links could
hit RPC node timeouts on view calls.

**Mitigation (deployed):**
- `maxIncomingEdges` (default 64): limits incoming edges processed per
  `effectiveVSRay` call. Edges beyond this limit are silently skipped.
- `maxOutgoingLinks` (default 64): limits outgoing links summed when
  computing a parent's link stake distribution.
- Both are governance-configurable via `ScoreEngine.setEdgeLimits()`.

**Remaining risk:** With both limits at 64 and depth 32, worst-case gas
is still significant. If RPC timeouts occur, increase cache duration in
the backend indexer and compute effective VS off-chain from indexed data.

### 2. StakeEngine — Ghost Lots in SideQueue

**Status:** Mitigated. Governance compaction implemented.

**Issue:** When a lot's amount reaches zero (fully burned by adverse
VS), the lot remains in the `SideQueue.lots` array with `amount = 0`.
`_recomputeSideTotal` and `_applyEpoch` iterate over all lots
including zero-amount ghosts. Over time, this increases snapshot gas.

**Why it's bounded:** StakeEngine uses lot consolidation — one lot
per user per side per post. Ghost lots can only accumulate from unique
users who were fully burned out. A post would need thousands of
distinct users who all lost 100% of their stake to cause material
gas increase.

**Mitigation (deployed):**
- `compactLots(postId, side)`: governance-callable function that
  removes zero-amount lots using swap-and-pop. O(N) per call.
  Storage-compatible (doesn't change layout).
- Ghost lots are also rescaled during position rescale (A.8 in the
  claim-spec) so their positions stay bounded even before compaction.

**Recommendation:** Run compaction when any post exceeds ~100 ghost lots.

## Security: MM_PRIVATE_KEY (Accept for Testnet, Fix for Mainnet)

**Status:** Accepted risk for testnet. Must be addressed before mainnet.

**Issue:** The market maker's private key is loaded from an environment
variable and used directly in `mm_wallet.py` to sign on-chain transactions
(buy/sell fills, permit executions, relay gas payments). If this key is
compromised, an attacker controls all USDC reserves and VSP inventory.

**Current mitigations:**
- Key is in `.env` (gitignored, not committed)
- GCP VM has restricted SSH access
- Testnet funds are limited

**Required for mainnet:**
- **Option A:** Multisig treasury. The MM wallet becomes a multisig
  (e.g., Gnosis Safe). Fills require multiple signatures. This adds
  latency but eliminates single-key risk.
- **Option B:** HSM/KMS signing. Use GCP Cloud KMS or AWS KMS to hold
  the key. The app calls the KMS API to sign transactions. The key never
  exists in memory on the VM.
- **Option C:** Separate hot/cold wallets. The MM holds only a small
  float in a hot wallet (enough for a few hours of fills). The cold
  wallet holds the bulk of reserves and requires manual top-ups.

**Recommendation:** Option C for launch (simplest), migrate to B later.

## Addressed in Earlier Phases

- Stale/duplicate address files (Phase 1)
- mockUSDC.json log dump (Phase 1)
- deploy.sh volume wipe on upgrade (Phase 1)
- relay.py undefined variable (Phase 1)
- Documentation spec drift (Phase 2)
- ScoreEngineFuzz.t.sol OppositeSideStaked failures (Phase 3 — fixed
  by using dedicated challenger address in tests)
- Position rescale edge case: stakers clamped to zero rate after
  others withdraw (Phase 3 — fixed by post-snapshot _rescalePositions)
- Documentation drift: sMax decay rate, cycle handling, tranche
  terminology, KNOWN-ISSUES staleness (Phase 3 — this update)
