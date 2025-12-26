# AI Semantic Duplication Detection (Spec)

## Goal

When a user attempts to create a new claim, we should be able to **detect likely semantic duplicates** among existing claims and return a ranked list of matches (top‑K) with similarity scores.

This system is **advisory** (non-authoritative):
- It does **not** reject, merge, or mutate on-chain state.
- It provides **UI hints** and **API results** so the user can choose whether to reuse an existing claim or continue with a new one.

## Inputs (from Task 3.6 Indexing Model)

The dedupe service consumes the indexed corpus of claims:

Minimum fields:
- `claim_post_id` (uint256 as decimal string or bigint)
- `text` (original claim text)
- `normalized_text` (stable normalization from 3.6)
- `created_at` (timestamp)

Optional fields (future):
- language
- source metadata (wikipedia url, citation ids, etc.)

## Outputs

Given an input claim text, return:

```json
{
  "query": {
    "text": "Drug X is safe",
    "normalized_text": "drug x is safe",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dim": 384
  },
  "threshold": 0.80,
  "top_k": 10,
  "matches": [
    {
      "claim_post_id": "123",
      "text": "Drug X is safe.",
      "similarity": 0.92
    }
  ]
}
```

Notes:
- Similarity is cosine similarity in `[0, 1]`.
- `threshold` is advisory; clients can choose to show warnings at 0.80+ and “strong warnings” at 0.90+.

## Similarity policy (recommended defaults)

- `similarity >= 0.90`: “Very likely duplicate”
- `0.80 <= similarity < 0.90`: “Possibly duplicate”
- `< 0.80`: “Probably distinct”

These are empirical; tune once you have real data.

## Determinism & Versioning

The dedupe result can change when:
- the embedding model changes,
- normalization logic changes,
- corpus grows (more candidates).

To preserve predictability:
- Store and return `embedding_model` and `embedding_dim`.
- Version your normalization function (e.g. `norm_v=1`) and store it with rows.

## Security / Abuse considerations

- Rate limit public endpoints (per-IP / per-wallet).
- Input size limits (e.g. max 2–4 KB text).
- Cache embeddings for repeated queries.
- Ensure DB indexes exist (pgvector `ivfflat` / `hnsw`) to avoid full scans.

## “Artifacts” (non-text claims)

Artifacts are **optional** and **off-chain**.
For 4.1, treat non-textual artifacts as:
- additional metadata attached to a claim (e.g., `artifact_uri`, `mime_type`)
- OR future work: perceptual hashes / vision embeddings

For now, 4.1 only dedupes **text**.

