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

4. **sMax tracks the leader; fallback decay only when empty.** A top-3
   leader tracker snaps `sMax` to the largest active post's total during
   normal operation; there is no slow decay while any post is active.
   A governance-configurable fallback exponential decay
   (`sMaxDecayRateRay = 9e17`, i.e. 10% per epoch, capped at
   `sMaxDecayMaxEpochs = 30`) only runs in the corner case where every
   post has zero stake, so sMax cannot stay frozen forever after a
   complete unwind.

5. **Minimum rate is 0.** The deployed StakeRatePolicy has
   `stakeIntRateMinRay = 0`. References to a 1% minimum are aspirational.

6. **Continuous midpoint positional weighting; per-lot independent
   rate.** The StakeEngine uses
   `weightedPosition = cumBefore + amount/2` and
   `positionWeight = 1 - (weightedPosition / sideTotal)`, applied
   independently per lot with no side-wide budget redistribution.
   A sole staker earns rBase/2; the first of many earlier stakers
   approaches rBase. The earlier `numTranches` storage variable and
   `setNumTranches` setter have been **fully removed** in StakeEngine
   v3 — the contract does not expose any tranche-related storage or
   ABI surface.

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

11. **Bounded fan-in: stake-desc sort + linkPostId-asc tiebreak.** When
    a claim has more incoming edges than `maxIncomingEdges`, or a parent
    has more outgoing links than `maxOutgoingLinks`, the ScoreEngine
    sorts those edges by link stake descending (with ties broken by
    linkPostId ascending — older link wins) and processes only the top
    N. Off-chain indexers must apply the same sort-and-cap rule with
    the same tiebreak when recomputing scores.

12. **Conservation of influence under bounded fan-out.** A link outside
    its parent's top-`maxOutgoingLinks` outgoing links contributes zero
    to its target's effective VS — it does not appear in either the
    parent's denominator (sumOutgoingLinkStake) or a numerator. This
    preserves the whitepaper §4.4 invariant that the sum of `linkShare`
    across a parent's outgoing links is ≤ 1.0 even when the parent has
    more outgoing links than the cap. Implemented by ScoreEngine v2.1
    (`_isInTopN` gate in `_computeEdgeContribution`).

## Last Updated

Phase 4 — full doc-vs-code reconciliation plus a protocol change.
Aligned all docs with the deployed StakeEngine v3 (midpoint weighting,
per-lot independent rate, no redistribution; setStake/setSMaxDecayRate/
setSMaxDecayMaxEpochs/rescanSMax/getTopPosts/getUserLotInfo entrypoints;
numTranches removed; sMax snap-to-leader with fallback-only decay;
withdraw recomputes positions; MAX_CLAIM_LENGTH = 2000 bytes). Promoted
ScoreEngine to v2.1: outgoing-link bound now sorts by stake desc with
linkPostId-ascending tiebreak (matching the existing incoming bound);
links outside the parent's top-N contribute zero, preserving
conservation of influence (whitepaper §4.4) under bounded fan-out;
public getEdgeContribution view also gates on the incoming top-N so
its result matches what effectiveVSRay would see.
