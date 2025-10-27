# VeriSphere: The Game of Staked Truth – A Decentralized Knowledge Market

White Paper  
Version 10.0  
Date: October 10, 2025  
Authors: VeriSphere Development Team  
Contact: info@verisphere.co

## Abstract

VeriSphere turns the search for verified knowledge into a high-stakes game, where users stake VSP tokens on claims to build a dynamic market of truth. This Solana-based dApp lets you post assertions, wager VSP to agree or challenge them, and profit from aligning with community consensus—while losing for misalignment. It collates Wikipedia, Quora, Reddit, and more, but overrides with staked validations to deliver the most accurate responses. VSP mints and burns dynamically, with rates favoring early bets. Relations link posts as supports or conflicts, weighting Verity Scores by staked connections. As a prediction market, it enables perpetual wagers on evolving knowledge. Fees like the 1 VSP posting cost stay pegged to gold's value. VeriSphere gamifies truth, rewarding sharp verity-seekers in a decentralized arena.

## Introduction

In an era of rampant misinformation, centralized platforms like Wikipedia and Quora struggle with bias, outdated content, and lack of incentives for accuracy. Prediction markets like Polymarket offer speculation but lack integration with knowledge curation. VeriSphere addresses these by turning verity-seeking into a game where users stake VSP tokens on posts, gaining for true or well-liked content and losing for false or disliked ones. The app collates external sources but modifies them with staked user changes, creating a living encyclopedia that "remembers" community refinements. Outcomes evolve perpetually, reflecting total stakes and linked influences. Fees adjust dynamically to VSP's value, ensuring accessibility. Governance is community-driven, with changes proposed and voted on by VSP holders.

## Problem Statement

* Misinformation Persistence: Without economic costs, false content spreads unchecked. VeriSphere counters this by imposing staking risks, where misaligned stakes burn VSP, deterring spam.

* Lack of Incentives: Contributors aren't rewarded for accuracy or penalized for errors. VeriSphere rewards aligned stakes with minting and burns misaligned ones, incentivizing truth-seeking.

* Fragmented Knowledge: External sources aren't unified or refined by user consensus. VeriSphere integrates them but modifies with VS stakes, creating a consensus-driven graph.

* Static Systems: Platforms don't adapt continuously to new stakes or evidence. VeriSphere's perpetual staking and real-time Verity Scores enable ongoing refinement.

* Prediction Market Limitations: Existing markets focus on binary events, not ongoing knowledge debates. VeriSphere extends prediction markets to perpetual binary claims.

VeriSphere solves these by making staking the core mechanic, with variable rewards to boost participation on under-staked topics.

## VeriSphere Overview

VeriSphere is a dApp with a content-first browser interface at verisphere.co, where users search or chat-query for information, receiving collated responses prioritized by staked consensus. Key features:

* Searchable Knowledge Graph: Posts indexed for quick retrieval, ranked by Verity Scores from stakes.

* Threaded Relations: Posts link as supports, conflicts, with stakes influencing connected Verity Scores.

* Continuous Mechanics: Stakes update Verity Scores in real-time, with variable interest rates.

* AI Collation: Prioritizes internal data, modifying external sources with staked changes. For example, for "solar sustainable," VS data overrides Wikipedia if staked Verity >0.7.

* Prediction Market Integration: Perpetual staking on claims, with odds views for speculation.

* Token Incentives: Uncapped VSP tokens mint for aligned stakes, burn for misaligned, with higher rates for low-stake posts.

The platform competes with prediction markets by allowing bets on knowledge claims (e.g., "Solar power is sustainable") without final resolution.

## User Interface and Visibility Mechanics

The VeriSphere UI is designed to prioritize verified, high-engagement content while de-emphasizing low-quality posts in an egalitarian manner, based solely on a post's total stake and Verity Score. This ensures that visibility is merit-based, rewarding accurate and popular contributions without shadow banning or arbitrary moderation.

* Visibility Algorithm: A post's visibility in searches, feeds, and recommendations is determined by a score combining its total stake (sum of agree and disagree VSP) and Verity Score (agree / total). Specifically, visibility_score = total_stake * Verity Score, with higher scores boosting prominence (e.g., top-ranked in results). Low stake/low Verity posts (e.g., Verity <0.5 and total <10 VSP) receive lower visibility, appearing further down in lists or requiring explicit filters to view. This egalitarian approach ensures all posts remain accessible (e.g., via direct links or advanced search), but the market (stake + Verity) naturally surfaces quality content.

* UI Elements: The content-first interface displays posts with Verity gauges, stake breakdowns, and relation graphs (D3.js). High-visibility posts appear in personalized feeds, while low ones are demoted but not hidden. Prediction market odds are shown for speculative claims, with stake prompts to engage.

* Rationale: This mechanic gamifies discovery, incentivizing staking on promising posts to increase their reach, while low-engagement content fades organically, maintaining a clean user experience without censorship.

## Game Mechanics and Logic

Posting and Staking

* Posting: Users create claims or answers (e.g., "Solar energy is sustainable"). Posting incurs a 1 VSP fee (equal to $1 at launch) to discourage spam without being prohibitive. This fee adjusts dynamically to VSP's market value, so that it remains constant relative to the price of gold (via an oracle). The fee is counted as stake for the purposes of the post's Verity Score, but it earns no interest.

* Interest Rate: Users add stake to upvote/like/agree/support a post, or to downvote/unlike/disagree/oppose a post. Stakes can be readjusted at any time by adding, removing, or switching sides. Interest is earned (via minting) on stake if it "aligns", and it’s lost (via burning) if it “misaligned”. The earn/loss rates are inversely proportional to the total stake per post, ranging from a maximum rate for a post’s 1st stake (a post with zero stake), to a (near) minimum rate for stake on posts with the highest stakes. At release, 10 times the US 10-Year Treasury Note (US10Y) will be used for the maximum rate, while 1/10th of the US10Y will be the minimum rate. Rates are subject to change, based on governance. Unstaked balances lose at the minimum rate.

* Updates: Users can't overwrite posts (blockchain immutability). Instead, they may create a new version of a post. They may link it to the original version, using the linking rules. Users may elect to migrate their stakes to the new version.

* Deletes: No permanent deletion, as all data is immutable for transparency.

Verity Score Calculation

* Basic Tally: Each post has a Verity Score calculated as agree_stake / (agree_stake + disagree_stake). For example, 10 VSP agree and 5 VSP disagree yields a score of 0.67. Scores update in real-time with every new stake or readjustment.

* Rewards/Penalties: Aligned stakes (Verity Score >0.5) mint new VSP at the variable rate, accruing directly to the stake. Misaligned stakes burn at the negative rate, diminishing value.

Relations and Stake Flow

* Relation Types: Links between posts are called "Relations," categorized as:

  * Supports: A post that agrees or builds on another (e.g., evidence reinforcing a claim).

  * Conflicts: A post that contradicts another (e.g., "sustainable" vs. "unsustainable").

* Stake Flow Logic: Stakes don't stay isolated—total agree/disagree from linked posts influence each other:

  * Supports: The Verity Score (VS) for dependent post B is calculated as B_agree + (A_VS * Link_upvotes) / (B_total + A_VS * Link_total). For example, assume that post B has 10 upvotes vs. 5 downvotes (B_agree = 10, B_total = 15). Post A has 60 up vs. 20 down (A_agree = 60, A_total = 80). A user creates a link from A to B, and upvotes it 5. Another user downvotes it 2. The VS yield for B = (10 + 0.75 * 5) / (15 + 0.75 * 7) = 13.75 / 20.25 ≈ 0.68. This formula weights the link by A's VS, and link downvotes dilute the total, ensuring that links are only as strong as their backing.

  * Conflicts: Similar to supports, but subtractive: B_agree - (A_VS * Link_upvotes) / (B_total + A_VS * Link_total).

AI Integration and Collation

* Query Handling: Home page search bar accepts questions ("Is solar sustainable?") or titles. AI (fine-tuned LLM) processes via NLP.

* Workflow:

  * Prioritize VS data: If staked posts cover the query (Verity Score >0.7), serve directly with stake metrics.

  * If incomplete, search web (Wikipedia, etc.), then modify: Override facts with VS stakes (e.g., "Wikipedia says X, but VS stakes correct to Y with 1,200 VSP agree").

* Response: Chat-like, with stake prompts to refine.

Tokenomics

* VSP Token: Uncapped, minted/burned based on alignment. Initialized to $1 per token at release (1 VSP = $1, pegged to gold value via Chainlink XAU/USD oracle for dynamic adjustments).

Development Process and Bounty System
VeriSphere is developed as an open-source project on GitHub (github.com/verisphere), with a browser interface at verisphere.co. The development process is bounty-driven, allowing solo and community contributions without a legal entity. Tasks are broken into modular bounties on Gitcoin, paid in VSP from the treasury wallet. Bounties are paid solely by VSP issuance, minted on-demand from the treasury contract.

* Completed Tasks: White Paper, Project Plan, Technical Architecture, Domain Acquisition (verisphere.co) and GitHub Setup are completed (with VSP payments logged in a public Google Sheet for transparency).

* Bounty System: Tasks are posted on Gitcoin, with VSP rewards (e.g., 800 VSP for Staking Contract). Contributors submit PRs; approvals trigger payments via wallet transfers. This ensures public development, with the founder logging solo work for VSP (e.g., white paper, project plan, technical architecture, domain setup, etc.). Bounties scale quadratically: p(n) = 100 + 500,000 / n VSP per hour, where n is cumulative hour sequence. For example, the first hour earns 500,100 VSP, the 2nd earns 250,100 VSP, etc. approaching 100 VSP/hour. Each task's bounty = sum(p(n) over its hours), assuming series completion.

Roadmap

* Q4 2025: Core mechanics.

* Q1 2026: AI launch.

* Q2 2026: Full app.

Conclusion
VeriSphere empowers users to refine knowledge through staking, with mechanics ensuring perpetual evolution and verity-seeking. Visit verisphere.co. 
