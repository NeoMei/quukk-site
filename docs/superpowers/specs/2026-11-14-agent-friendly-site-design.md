# Agent-friendly Website Design

## Goal
Make the quukk static site easier for crawlers and language models to discover, interpret, verify, and cite while preserving the current human-facing design.

## Scope
- Add a curated `/llms.txt` discovery page and a machine-readable `/agent-manifest.json`.
- Add stable product detail pages in Chinese and English, with Markdown and JSON variants for agent consumption.
- Make key scenario content present in static HTML even when JavaScript is disabled.
- Expand JSON-LD with per-product software entities, dates, and evidence/status fields that are also visible in page copy.
- Clarify crawler policy without treating `robots.txt` as security control.

## Non-goals
- No unauthenticated business actions, API, or MCP endpoint is invented.
- No claim that marketing screenshots are production acceptance evidence.
- No redesign of the existing visual style.
