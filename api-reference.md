# VeriSphere API Reference

Base URL: `https://<host>/api` (or `http://localhost:8070/api` for local development)

All endpoints return JSON. Errors return `{"detail": "error message"}` with appropriate HTTP status codes.

---

## Health

### `GET /healthz`

Health check.

**Response:** `{"ok": "true"}`

---

## Articles

### `GET /api/article/{topic}`

Get a full article with VS-enriched sentences. Serves from pre-built cache (sub-50ms). If no article exists, generates one (10–30s on first visit).

**Parameters:**
- `topic` (path, required): Topic name (URL-encoded). Case-insensitive.

**Response:**
```json
{
  "article_id": 1,
  "title": "Climate Change",
  "topic_key": "climate change",
  "sections": [
    {
      "section_id": 10,
      "heading": "Overview",
      "sentences": [
        {
          "sentence_id": 42,
          "sort_order": 0,
          "text": "The primary driver of modern climate change is...",
          "post_id": 2,
          "replaced_by": null,
          "stake_support": 3.01,
          "stake_challenge": 0.0,
          "verity_score": 100.0
        }
      ]
    }
  ]
}
```

Sentences with `post_id: null` are AI-generated but not yet on-chain. Sentences with a `post_id` are registered claims with live VS/stake data.

### `GET /api/article/{topic}/version`

Return the current article cache hash. Frontend polls this every 30s to detect updates.

**Response:** `{"hash": "a1b2c3d4e5f6g7h8"}` or `{"hash": null}` if no article exists.

### `POST /api/article/{topic}/generate`

Generate (or regenerate) an article. Idempotent — returns cached version if `refresh: false`.

**Body:**
```json
{"refresh": false}
```

### `POST /api/article/{topic}/refresh`

Regenerate article content and merge with existing. Preserves all existing sentences and on-chain links. Triggers cache rebuild.

**Response:** `{"refreshed": true, "topic": "climate change"}`

### `POST /api/article/sentence/insert`

Insert a new sentence into a section.

**Body:**
```json
{
  "section_id": 10,
  "after_sentence_id": 42,
  "text": "New claim text here."
}
```

`after_sentence_id` is optional — if null, inserts at the beginning of the section.

**Response:**
```json
{
  "inserted": [
    {"sentence_id": 99, "text": "New claim text here.", "post_id": null}
  ]
}
```

### `POST /api/article/sentence/{sentence_id}/edit`

Replace a sentence. Creates new sentence(s) and marks the old one as replaced. If the new text is semantically different, it may be placed in a different section.

**Body:**
```json
{"new_text": "Corrected claim text."}
```

**Response:**
```json
{
  "old_sentence_id": 42,
  "old_post_id": 2,
  "created": [
    {"sentence_id": 100, "text": "Corrected claim text.", "post_id": null}
  ]
}
```

The frontend is responsible for creating the on-chain challenge link (new challenges old) via the user's wallet.

### `POST /api/article/sentence/{sentence_id}/link_post`

Link a sentence to its on-chain post_id after client-side registration. Triggers article cache rebuild.

**Body:** `{"post_id": 16}`

**Response:** `{"sentence_id": 99, "post_id": 16}`

### `POST /api/article/sentence/{sentence_id}/register`

Deprecated. Returns 501. Use `/link_post` instead.

### `POST /api/article/sentence/cleanup`

AI grammar/spelling cleanup. Returns original and suggested text.

**Body:**
```json
{"text": "Teh earth is round.", "topic": "geography"}
```

**Response:**
```json
{"original": "Teh earth is round.", "suggested": "The earth is round."}
```

Rate-limited (AI endpoint).

---

## Claims

### `GET /api/claims/fast/all`

Fast claims list using indexed DB data (no RPC calls). Primary endpoint for the Claims Explorer.

**Parameters:**
- `limit` (query, optional): Max results. Default 500.

**Response:**
```json
{
  "claims": [
    {
      "post_id": 7,
      "text": "COVID-19 originated at the Wuhan Institute of Virology.",
      "creator": "0x49E0...C4d3",
      "verity_score": 38.94,
      "base_vs": 81.66,
      "stake_support": 22.14,
      "stake_challenge": 4.97,
      "total_stake": 27.11,
      "controversy": 0.18,
      "incoming_links": 3,
      "outgoing_links": 1,
      "topic": "covid-19",
      "created_at": null
    }
  ],
  "total": 17,
  "total_stake": 49.3,
  "avg_vs": 52.2
}
```

`verity_score` is the effective VS (includes link propagation). `base_vs` is the raw stake-based VS before link effects.

### `GET /api/claims/all`

Deprecated. Delegates to `/fast/all`.

### `GET /api/claims/search`

Search claims by text.

**Parameters:**
- `q` (query, required): Search query.
- `limit` (query, optional): Max results. Default 10.

**Response:** `{"claims": [...]}`

### `GET /api/claims/{post_id}/summary`

Detailed summary for a single claim.

### `GET /api/claims/{post_id}/stakes`

Stake totals and optional user-specific stakes.

**Parameters:**
- `post_id` (path, required): On-chain post ID.
- `user` (query, optional): User address for position lookup.

**Response:**
```json
{
  "post_id": 6,
  "stake_support": 20.15,
  "stake_challenge": 1.24,
  "verity_score": -4.04,
  "user_support": 0.0,
  "user_challenge": 1.24
}
```

### `GET /api/claims/{post_id}/user-stake`

User's specific stake on a claim. Lighter than `/stakes`.

**Parameters:**
- `post_id` (path, required)
- `user` (query, optional): User address.

**Response:** `{"user_support": 0.0, "user_challenge": 1.24}`

### `GET /api/claims/{post_id}/edges`

Evidence graph edges (incoming and outgoing links) for a claim.

**Parameters:**
- `post_id` (path, required)
- `direction` (query, optional): `incoming` or `outgoing`. If omitted, returns both.

**Response:**
```json
{
  "incoming": [
    {
      "claim_post_id": 3,
      "link_post_id": 4,
      "is_challenge": false,
      "claim_text": "Milankovitch cycles are the primary driver...",
      "claim_vs": 100.0,
      "claim_support": 5.02,
      "claim_challenge": 0.0,
      "link_support": 2.0,
      "link_challenge": 0.0,
      "link_vs": 100.0
    }
  ],
  "outgoing": [
    {
      "claim_post_id": 2,
      "link_post_id": 5,
      "is_challenge": true,
      "claim_text": "The primary driver of modern climate change...",
      "claim_vs": -100.0,
      "claim_support": 0.0,
      "claim_challenge": 0.0,
      "link_support": 1.0,
      "link_challenge": 0.0,
      "link_vs": 100.0
    }
  ]
}
```

An **incoming** edge means another claim provides evidence for/against this claim. An **outgoing** edge means this claim provides evidence for/against another claim. `is_challenge: true` means the link argues against; `false` means it supports.

### `GET /api/claims/{post_id}/debug`

Debug endpoint showing raw on-chain data for VS calculation.

### `GET /api/claims/check-onchain`

Check if a claim text already exists on-chain.

**Parameters:**
- `text` (query, required): Claim text.

**Response:** `{"exists": true, "post_id": 16}` or `{"exists": false, "post_id": null}`

### `GET /api/claim-status/{claim_text}`

Full claim state including on-chain stakes and verity score.

**Parameters:**
- `claim_text` (path, required): URL-encoded claim text.
- `user` (query, optional): User address.

### `POST /api/claims/create`

Create a claim on-chain (server-side, uses MM wallet). Prefer the relay for gasless user-initiated claims.

**Body:** `{"text": "Claim text here."}`

**Response:** `{"tx_hash": "0x..."}`

### `POST /api/claims/record`

Record a claim's on-chain post_id in the local DB. Called by frontend after a successful on-chain creation.

**Body:** `{"text": "Claim text", "post_id": 16}`

### `POST /api/claims/stake`

Stake on a claim (server-side, uses MM wallet).

**Body:**
```json
{"claim_id": 6, "side": "support", "amount": 10}
```

### `POST /api/claims/unstake`

Withdraw stake from a claim (server-side).

**Body:**
```json
{"claim_id": 6, "side": "challenge", "amount": 5, "lifo": true}
```

### `POST /api/claims/detect-topic`

Auto-detect topic for a standalone claim, store the association, and trigger background article generation if needed.

**Body:** `{"claim_text": "The Torah is...", "post_id": 19}`

**Response:** `{"topic": "religion", "status": "ok"}`

---

## Evidence Links

### `POST /api/links/create`

Create an evidence link between two on-chain claims.

**Body:**
```json
{
  "independent_post_id": 3,
  "dependent_post_id": 1,
  "is_challenge": false
}
```

`independent_post_id` is the evidence provider. `dependent_post_id` is the claim being supported/challenged.

---

## Market Maker

### `GET /api/mm/quote`

Current spot prices (indicative — actual fills use volume integration).

**Response:**
```json
{
  "mid_price_usd": 2.81,
  "buy_price_usd": 2.82,
  "sell_price_usd": 2.80,
  "floor_price_usd": 1.73,
  "ts": "2026-04-03T12:05:12Z"
}
```

The pricing formula is `log10(net_vsp + 10)² × unit_au × gold_usd` where `unit_au = 0.0001` troy oz. Buy/sell prices include a 0.25% half-spread.

### `GET /api/mm/floor`

Liquidation floor price (publicly documented).

**Response:**
```json
{
  "floor_price_usd": 1.73,
  "usdc_reserves": 475.83,
  "vsp_circulating": 274.68,
  "ts": "2026-04-03T12:05:12Z"
}
```

### `GET /api/mm/preview-buy`

Preview a buy order with fee breakdown.

**Parameters:**
- `qty_vsp` (query): Amount of VSP to buy.
- `usdc_amount` (query): Alternatively, specify USDC budget.

**Response:**
```json
{
  "qty_vsp": 10.0,
  "total_usdc": 13.23,
  "fee_vsp": 0.57,
  "fee_usdc": 0.72,
  "avg_price": 1.25,
  "breakdown": "base: 0.44 + 30% margin: 0.13 = 0.57 VSP ($0.75)"
}
```

### `GET /api/mm/preview-sell`

Preview a sell order with fee breakdown.

**Parameters:**
- `qty_vsp` (query, required): Amount of VSP to sell.

### `POST /api/mm/preview`

Generic fill preview (buy or sell).

**Body:** `{"side": "buy", "qty_vsp": 10.0}`

### `POST /api/mm/buy`

Execute a VSP buy. If `permit` is provided, the MM executes USDC.permit() gaslessly. Otherwise requires existing allowance.

**Body:**
```json
{
  "user_address": "0x49E0...C4d3",
  "qty_vsp": 10.0,
  "max_total_usdc": 15.0,
  "permit": {
    "deadline": 1712345678,
    "v": 28,
    "r": "0x...",
    "s": "0x...",
    "value": 15000000
  }
}
```

`permit` is optional. `max_total_usdc` is slippage protection.

**Response:**
```json
{
  "ok": true,
  "qty_vsp": 10.0,
  "fee_vsp": 0.57,
  "fee_usdc": 0.72,
  "gross_usdc": 12.51,
  "total_usdc": 13.23,
  "avg_price_usd": 1.2514
}
```

### `POST /api/mm/sell`

Execute a VSP sell. Same structure as buy but user sends VSP and receives USDC.

### `GET /api/mm/permit-nonce/{token}/{address}`

Get the current EIP-2612 permit nonce for signing.

---

## Relay (Gasless Meta-Transactions)

### `POST /api/relay`

Submit a signed EIP-712 meta-transaction. The relay pays gas; user only signs. Supports optional EIP-2612 permits for token approvals.

**Body:**
```json
{
  "request": {
    "from": "0x49E0...C4d3",
    "to": "0xd639...13d9",
    "value": 0,
    "gas": 600000,
    "nonce": 5,
    "deadline": 1712345678,
    "data": "0x4a3e1b89..."
  },
  "signature": "0x...",
  "permit": null,
  "fee_permit": null
}
```

`permit` (optional): EIP-2612 permit for the token being staked (grants StakeEngine allowance).
`fee_permit` (optional): EIP-2612 permit granting the Forwarder VSP allowance for the relay fee.

**Response (success):**
```json
{
  "ok": true,
  "tx_hash": "0x...",
  "claim": {
    "post_id": 16,
    "text": "Claim text...",
    "creator": "0x49E0...C4d3",
    "support_total": 0,
    "challenge_total": 0,
    "user_support": 0,
    "user_challenge": 0
  }
}
```

The `claim` field is present for createClaim and stake operations. For createClaim, it also includes `text` and `creator`. For duplicate claims, `duplicate: true` is set.

**Response (error):**
```json
{"detail": "Transaction reverted on-chain. Common causes: insufficient VSP balance, duplicate claim, or contract error."}
```

### `GET /api/relay/nonce/{address}`

Get the current forwarder nonce for constructing meta-transactions.

**Response:** `{"nonce": 5}`

---

## Fees

### `GET /api/fees`

Full fee schedule with cost breakdown and examples.

**Response:**
```json
{
  "costs": {"gcp_server": 200.0, "rpc_provider": 49.0, "anthropic": 80.0, ...},
  "total_monthly_usd": 574.0,
  "expected_monthly_txns": 1000,
  "vsp_price_usd": 1.3,
  "per_txn_cost_usd": 0.574,
  "base_fee_vsp": 0.44,
  "pct_fee_bps": 100,
  "margin_bps": 3000,
  "enabled": true,
  "examples": {...}
}
```

### `GET /api/fees/estimate`

Estimate fee for a specific transaction type.

**Parameters:**
- `tx_type` (query, required): `buy`, `sell`, `stake`, `create`, etc.
- `value_vsp` (query, optional): Transaction value. Default 1.0.

### `POST /api/fees/costs` (Admin)

Update an operating cost. Requires `X-Admin-Key` header.

**Parameters:**
- `cost_key` (query): e.g. `gcp_server`
- `monthly_usd` (query): New monthly cost in USD.

### `POST /api/fees/params` (Admin)

Update a fee parameter. Requires `X-Admin-Key` header.

**Parameters:**
- `param_key` (query): e.g. `margin_bps`
- `value` (query): New value.

---

## Portfolio

### `GET /api/portfolio/fast/{address}`

Fast portfolio using indexed DB data (no RPC calls).

**Parameters:**
- `address` (path, required): Wallet address.

### `GET /api/portfolio/{address}`

Full portfolio with live on-chain data (slower, makes RPC calls).

---

## Tokens

### `GET /api/token/balance`

Read VSP token balance.

**Parameters:**
- `address` (query, required): Wallet address.

**Response:** `{"balance": "100000000000000000000"}` (wei)

### `GET /api/token/allowance`

Read VSP token allowance.

**Parameters:**
- `owner` (query, required)
- `spender` (query, required)

**Response:** `{"allowance": "0"}` (wei)

---

## Supersedes

Claim supersession protocol — propose that one claim replaces another.

### `POST /api/supersede`

Create a supersession proposal.

**Body:**
```json
{
  "old_post_id": 1,
  "new_post_id": 16,
  "created_by": "0x49E0...C4d3"
}
```

### `GET /api/supersedes/pending/{address}`

Get pending supersession proposals for a user.

### `POST /api/supersedes/respond`

Accept or reject a supersession proposal.

**Body:**
```json
{
  "supersede_id": 1,
  "user_address": "0x49E0...C4d3",
  "response": "accept"
}
```

---

## Other

### `GET /api/contracts`

All deployed contract addresses.

**Response:**
```json
{
  "Authority": "0x9a9f...",
  "VSPToken": "0x5803...",
  "PostRegistry": "0xd639...",
  "LinkGraph": "0x117f...",
  "StakeEngine": "0xb551...",
  "ScoreEngine": "0x8010...",
  "ProtocolViews": "0x793d...",
  "USDC": "0x5425...",
  "Forwarder": "0xf1b8..."
}
```

### `GET /api/disambiguate`

Typeahead search for the topic search bar.

**Parameters:**
- `q` (query, required): Search query (min 1 character).

**Response:** `{"results": [{"key": "climate change", "title": "Climate Change"}, ...]}`

### `GET /api/topics/popular`

Most-viewed topics for the landing page.

**Parameters:**
- `limit` (query, optional): Max results. Default 8.

**Response:**
```json
{
  "topics": [
    {"key": "israel", "title": "Israel", "views": 115},
    {"key": "climate change", "title": "Climate Change", "views": 50}
  ]
}
```

### `POST /api/moderate`

Check if content passes moderation.

**Body:** `{"text": "Content to check", "topic": ""}`

**Response:** `{"allowed": true, "reason": null}` or `{"allowed": false, "reason": "Content blocked: ..."}`

### `POST /api/reindex/{post_id}`

Trigger immediate reindex of a post. Admin/debug utility.

**Parameters:**
- `post_id` (path, required)
- `user` (query, optional): Also reindex this user's stakes.

**Response:** `{"ok": true, "post_id": 16}`

---

## Authentication

Most endpoints are public. Two endpoints require the `X-Admin-Key` header:

- `POST /api/fees/costs`
- `POST /api/fees/params`

Set the admin key via the `ADMIN_API_KEY` environment variable.

## Rate Limiting

AI-powered endpoints (`/generate`, `/cleanup`) are rate-limited. The relay endpoint (`/api/relay`) has its own rate limiter to prevent gas abuse.

## On-Chain Integration

The API backend connects to Avalanche C-Chain (Fuji testnet, chain ID 43113). Contract addresses are returned by `/api/contracts`. The relay uses an ERC-2771 meta-transaction forwarder for gasless operations.

All VSP amounts in the API are in human-readable units (not wei), except `/api/token/balance` and `/api/token/allowance` which return wei strings for precision.
