# VeriSphere Known Issues & Future Work

## Gas Concerns (Non-Urgent, Monitor)

### 1. ScoreEngine.effectiveVSRay — Recursive Gas Cost

**Status:** Monitor. Not yet a problem at current scale.

**Issue:** `effectiveVSRay` recursively calls `getIncoming` and
`getOutgoing` across LinkGraph and StakeEngine, with depth up to 32.
Each level loads dynamic arrays from storage. A claim with many
incoming links from parents that each have many outgoing links could
hit RPC node timeouts on view calls.

**Risk level:** Low for MVP. The function is `view` (no on-chain gas
limit for eth_call), but RPC providers impose their own timeouts
(typically 10-30s). A claim with 50+ incoming links from parents with
20+ outgoing links each could exceed this.

**Proposed fix (future UUPS upgrade):**
- Add `MAX_INCOMING_EDGES` (e.g., 64) to `_sumIncomingContributions`.
  Process only the first N edges sorted by contribution magnitude.
- Add `MAX_OUTGOING_LINKS` (e.g., 64) to `_sumOutgoingLinkStake`.
- These limits would be governance-configurable.
- The off-chain indexer can compute unbounded effective VS for display;
  the on-chain version serves as a bounded approximation.

**Workaround (no contract change):** The backend already caches VS
via the chain indexer. If RPC timeouts occur, increase cache duration
and compute effective VS off-chain from indexed data.

### 2. StakeEngine — Ghost Lots in SideQueue

**Status:** Low risk. Bounded by unique users, not operations.

**Issue:** When a lot's amount reaches zero (fully burned by adverse
VS), the lot remains in the `SideQueue.lots` array with `amount = 0`.
`_recomputeSideTotal` and `_applyEpochTranched` iterate over all lots
including zero-amount ghosts. Over time, this increases snapshot gas.

**Why it's bounded:** StakeEngine v2 uses lot consolidation — one lot
per user per side per post. Ghost lots can only accumulate from unique
users who were fully burned out. A post would need thousands of
distinct users who all lost 100% of their stake to cause material
gas increase.

**Proposed fix (future UUPS upgrade):**
- Option A: Add a governance-callable `compactLots(postId, side)`
  that removes zero-amount lots and re-indexes the lot mappings.
  Storage-compatible (doesn't change layout).
- Option B: During withdrawal, if `lot.amount == 0` after the
  withdrawal, swap-and-pop the lot from the array. Requires updating
  `lotIndex` mappings for the swapped lot.
- Option C: Skip zero-amount lots in `_applyEpochTranched` (already
  done via `if (lot.amount == 0) continue`) but also skip them in
  `_recomputeSideTotal` by maintaining a running total instead of
  re-summing. This is a logic change, not a storage change.

**Recommendation:** Option A (governance compaction) is safest and
storage-compatible. Implement when any post exceeds ~100 ghost lots.

## Test Hygiene (Completed)

### Duplicate Mock Definitions — Fixed

Inline MockVSP and MockPostingFeePolicy definitions in
LinkGraphAcyclic.t.sol, PostRegistry.t.sol, ScoreEngine.t.sol, and
StakeEngine.t.sol have been replaced with imports from test/mocks/.
The shared mocks in test/mocks/ are the single source of truth.

### Stale Test Assertions — Fixed

- `test_Acyclic_RevertsOnCycle` → `test_CyclesAreAllowed` (cycles permitted)
- `test_VSZeroBelowPostingFee` → fixed (baseVSRay doesn't check activity)
- `test_VS_Zero_BelowFee` → fixed (same root cause)
- `test_ClaimSummaryAndRawRays` → fixed (same root cause)
- `testSnapshotTriggersOnStakeAfterPeriod` → fixed (assertGt → assertGe)



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
