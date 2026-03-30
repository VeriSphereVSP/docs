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

2. **Base VS formula is asymmetric.** `ScoreEngine.baseVSRay` returns
   `+(A*RAY/T)` when support leads, `-(D*RAY/T)` when challenge leads.
   This differs from the symmetric `(2A/T - 1)` formula in some older text.

3. **sMax decays.** The global reference decays at 0.999 per epoch,
   preventing historical lock-in. Older docs that say "sMax only grows"
   are outdated.

4. **Minimum rate is 0.** The deployed StakeRatePolicy has
   `stakeIntRateMinRay = 0`. References to a 1% minimum are aspirational.

5. **Tranche-based positional weighting.** The StakeEngine v2 uses
   governance-configurable tranches (default 10), not the per-lot
   `mid/sMax` or `q_i/Q_max` formulas from earlier drafts.

## Last Updated

Phase 2 canonicalization — aligned all docs with StakeEngine v2 and
ScoreEngine code as deployed on Fuji testnet.
