# VeriSphere Documentation Status

## Document Hierarchy

| Document | Role | Authority |
|----------|------|-----------|
| `claim-spec-evm-abi.md` | **Normative** ABI + economic spec | Governs all economic details |
| `whitepaper.md` | Public-facing protocol description | Defers to claim-spec on formulas |
| `architecture.md` | Technical architecture overview | Defers to claim-spec on economics |
| `system-blueprint.md` | Full system design (protocol + app) | Defers to claim-spec on economics |
| `guide.md` *(frontend only)* | User-facing gameplay guide | App-layer; lives in `frontend/public/docs/` |

## Rule

If any document conflicts with `claim-spec-evm-abi.md` Appendix A on
economic formulas, rate computation, positional weighting, or sMax behavior,
the claim-spec governs. The Solidity code (`core/src/StakeEngine.sol`,
`core/src/ScoreEngine.sol`) is the ultimate source of truth; the claim-spec
tracks the code.

## Key Design Decisions Reflected in Code

1. **Link graph permits cycles.** The LinkGraph contract does not enforce
   a DAG. Cycles are handled by the ScoreEngine during VS computation
   using stack-based detection with a depth limit of 32.

2. **Cycle detection returns 0.** When a post is encountered on the
   computation stack, its contribution for that path is 0 (not its base VS).
   This is the most conservative behavior and prevents all self-influence.

3. **Base VS formula is asymmetric.** `ScoreEngine.baseVSRay` returns
   `+(A*RAY/T)` when support leads, `-(D*RAY/T)` when challenge leads.
   This differs from the symmetric `(2A/T - 1)` formula used internally
   by StakeEngine for rate sign determination. Both agree on sign.

4. **sMax decays at 0.5% per epoch.** `SMAX_DECAY_RATE_RAY = 995e15`.
   The global reference decays when the leading post's total stake falls
   below the previous sMax, preventing historical lock-in.

5. **Minimum rate is 0.** The deployed StakeRatePolicy has
   `stakeIntRateMinRay = 0`. References to a 1% minimum are aspirational.

6. **Continuous positional weighting.** The StakeEngine uses a continuous
   linear weight: `positionWeight = 1 - (weightedPosition / sideTotal)`.
   The `numTranches` storage variable exists for ABI compatibility but is
   not consulted by the reward math.

7. **Post-snapshot position rescale.** After each snapshot, all lots'
   `weightedPosition` values are mapped into `[0, sideTotal - 1)` to
   prevent the zero-rate edge case from withdrawal-induced position drift.

8. **Single-sided positions.** A user cannot hold stake on both sides of
   the same post. `OppositeSideStaked` reverts enforce this.

9. **Bounded fan-in.** ScoreEngine processes at most `maxIncomingEdges`
   (default 64) incoming links and `maxOutgoingLinks` (default 64) outgoing
   links per parent. Both are governance-configurable via `setEdgeLimits`.

10. **Ghost lot compaction.** `compactLots(postId, side)` is a governance-
    callable function that removes zero-amount lots via swap-and-pop.

## Last Updated

Phase 3 — aligned all docs with StakeEngine v2 (position rescale,
continuous weighting, single-sided positions), ScoreEngine v2
(bounded fan-in, cycle handling), and deployed Fuji testnet state.
