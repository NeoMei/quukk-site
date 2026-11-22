# Agent-friendly Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Make the quukk static site easier for agents and LLMs to discover, interpret, verify, and cite.

**Architecture:** Keep the existing static HTML/CSS/JS site. Add a curated discovery layer (`llms.txt`, `agent-manifest.json`), normalized product records rendered into bilingual HTML/Markdown/JSON detail pages, and consistent JSON-LD/evidence metadata. Keep all factual content statically present; JavaScript remains progressive enhancement only.

**Tech Stack:** Plain HTML, CSS, JavaScript, JSON, Markdown, Python standard library for generation/verification scripts.

**Spec:** `docs/superpowers/specs/2026-11-14-agent-friendly-site-design.md`

## Global Constraints

- Preserve the existing visual design and public routes.
- Do not claim or expose business actions that the site cannot actually execute.
- Keep Chinese and English product names, URLs, statuses, and timestamps consistent.
- Treat screenshots/examples as examples unless independently verified.
- Preserve existing user modifications and untracked design artifacts.

---

### Task 1: Add canonical product data and machine-readable discovery files

**Files:**
- Create: `data/agent-products.json`
- Create: `dist/agent-manifest.json`
- Create: `dist/llms.txt`
- Create: `dist/llms-full.txt`
- Create: `scripts/build-agent-assets.py`

**Interfaces:**
- `data/agent-products.json` is the source of truth for product ids, names, aliases, URLs, descriptions, capabilities, limits, status, evidence, and verification date.
- `scripts/build-agent-assets.py` reads the source data and writes deterministic manifest and llms files.

- [x] Define all seven public products with exact existing names and links; mark `actions` as an empty array unless an actual public action exists.
- [x] Include source/evidence and `last_verified` fields, distinguishing `public_description`, `interface_example`, and `user_provided_product_material`.
- [x] Generate `/agent-manifest.json` with schema version, site metadata, glossary links, products, and no fake API/MCP actions.
- [x] Generate `/llms.txt` as a concise curated index and `/llms-full.txt` as an explicitly non-standard convenience export.
- [x] Run the generator twice and verify byte-for-byte deterministic output.

### Task 2: Add bilingual product pages and machine-readable derivatives

**Files:**
- Create: `dist/products/*.html`
- Create: `dist/en/products/*.html`
- Create: `dist/products/*.md`
- Create: `dist/en/products/*.md`
- Create: `dist/products/*.json`
- Create: `dist/en/products/*.json`
- Modify: `scripts/build-agent-assets.py`

**Interfaces:**
- Every product id from `data/agent-products.json` has zh/en HTML, Markdown, and JSON outputs.
- HTML pages expose the same visible facts as JSON/Markdown and link to the official external product URL.

- [x] Generate pages with a fixed question-oriented structure: what it is, capabilities, limits, access, evidence, last verified.
- [x] Add `rel="alternate" type="text/markdown"` and JSON links to each HTML page.
- [x] Include `SoftwareApplication` JSON-LD with stable ids, `dateModified`, `sameAs`, and `isPartOf`.
- [x] Add product routes to sitemap with hreflang pairs.
- [x] Verify every generated internal and external URL is syntactically valid and every local asset exists.

### Task 3: Make homepage content consistent and statically discoverable

**Files:**
- Modify: `dist/index.html`
- Modify: `dist/en/index.html`
- Modify: `dist/glossary.html`
- Modify: `dist/en/glossary.html`
- Modify: `dist/sitemap.xml`
- Modify: `dist/robots.txt`

- [x] Correct stale “four tools” wording to match the five applications and two supporting platforms.
- [x] Add visible links to the product directory/agent manifest and detail pages.
- [x] Add `dateModified`, `BreadcrumbList`, and per-product `SoftwareApplication` entities to JSON-LD.
- [x] Keep all scenario panel copy in the static DOM; ensure JS only toggles visibility/selection.
- [x] Add crawler policy comments/configuration that preserves public indexing while documenting vendor-specific choices.
- [x] Add generated product URLs and glossary URLs to sitemap with accurate `lastmod`.

### Task 4: Add verification and documentation

**Files:**
- Create: `scripts/verify-agent-friendly-site.py`
- Modify: `site/README.md`
- Create: `docs/agent-friendly-site.md`

- [x] Verify required files, valid JSON, matching product ids/names/URLs, canonical/hreflang pairs, static text presence, and no stale “four tools” phrase.
- [x] Verify every generated HTML page contains a single h1, JSON-LD, status, evidence, and last-verified text.
- [x] Run a local HTTP server and curl key routes with JavaScript disabled conceptually (raw response) to confirm content is present.
- [x] Document how to update source product data and regenerate outputs.

### Task 5: Final validation

- [x] Run the generator.
- [x] Run the verification script.
- [x] Validate sitemap XML and JSON-LD parseability with standard-library checks.
- [x] Inspect git diff and ensure pre-existing modifications remain intact.
- [x] Report any claims that remain unverified instead of calling them complete.


## Verification evidence

- `python3 scripts/build-agent-assets.py` completed successfully.
- Generated outputs were byte-for-byte deterministic across repeated runs (46 files hashed).
- `python3 scripts/verify-agent-friendly-site.py` passed for 7 products.
- Local HTTP server returned 200 for homepage, English homepage, llms.txt, agent-manifest.json, product HTML/Markdown, sitemap.xml, and robots.txt.
- All checked JSON-LD blocks parsed successfully and homepage exposes 7 SoftwareApplication entities.
