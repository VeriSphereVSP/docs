# VeriSphere Architecture

**Version**: 1.0  
**Date**: October 27, 2025  
**Authors**: VeriSphere Development Team  
**Contact**: info@verisphere.co  
**Repository**: github.com/VeriSphereVSP/docs  

## Introduction

This document outlines the technical architecture of VeriSphere, a Solana-based decentralized application (dApp) that gamifies knowledge verification through staking VSP tokens on claims. The system integrates blockchain smart contracts for staking and relations, a Node.js backend for AI-driven collation, a React frontend for user interaction, and GCP for hosting. The architecture emphasizes decentralization, scalability, and AI enhancement, with open-source development via GitHub and bounty-driven contributions.

Key goals:
- Perpetual staking on knowledge claims for dynamic Verity Scores.
- AI collation of external sources modified by staked consensus.
- Egalitarian visibility based on stake and Verity without censorship.
- Tokenomics with mint/burn tied to alignment and gold peg.

## System Overview

VeriSphere is a full-stack dApp with the following layers:
- **Frontend**: React app for user queries, staking, and views.
- **Backend**: Node.js server for AI processing and API calls.
- **Blockchain**: Solana programs for VSP token, staking, relations.
- **Infrastructure**: GCP Cloud Run for deployment, BigQuery for data, Chainlink for oracles.
- **Tools**: Anchor for Solana contracts, GitHub Actions for CI/CD, Gitcoin for bounties.

### Architecture Diagram (Text-Based)
