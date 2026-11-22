# Agent-friendly site maintenance

The public site has two machine-facing layers:

- `dist/llms.txt` is a short, curated index for language models. It is a convenience convention, not an access-control or training opt-out mechanism.
- `dist/agent-manifest.json` is the structured catalog. It records product ids, names, official URLs, descriptions, capabilities, limits, status, evidence, and verification dates.

The source of truth is `data/agent-products.json`. Do not edit generated files by hand. After changing product facts, run:

```sh
python3 scripts/build-agent-assets.py
python3 scripts/verify-agent-friendly-site.py
```

The generator also writes bilingual product derivatives under `dist/products/` and `dist/en/products/`. The manifest links each product's HTML, Markdown, and JSON variants. Each product page must expose the same facts in visible HTML, Markdown, JSON, and JSON-LD.

Factual boundaries:

- `status` describes the evidence level, not a promise of availability.
- `evidence.kind` distinguishes public descriptions, interface examples, and user-provided product material.
- An interface screenshot is not production acceptance evidence unless the record explicitly says so.
- `actions` stays empty until a real public, authenticated operation exists. Do not add invented API or MCP actions to improve discoverability.
- `last_verified` is the date the public fact was last checked; update it when the source or product behavior changes.

The static site remains readable with JavaScript disabled. JavaScript may enhance menus, tabs, and image viewers, but it must not be the only place where product identity, capabilities, limitations, or access information exists.
