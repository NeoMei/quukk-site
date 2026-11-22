#!/usr/bin/env python3
"""Generate deterministic agent discovery assets from data/agent-products.json."""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "agent-products.json"
DIST = ROOT / "dist"
SM_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"
ET.register_namespace("", SM_NS)
ET.register_namespace("xhtml", XHTML_NS)


def load_source() -> dict[str, Any]:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1":
        raise ValueError("unsupported schema_version")
    if not isinstance(data.get("products"), list) or not data["products"]:
        raise ValueError("products must be a non-empty list")
    ids: set[str] = set()
    required = {
        "id", "category", "name_zh", "name_en", "url", "description_zh",
        "description_en", "capabilities", "limits", "status", "last_verified",
        "evidence", "actions",
    }
    for product in data["products"]:
        missing = required - set(product)
        if missing:
            raise ValueError(f"{product.get('id', '<unknown>')} missing {sorted(missing)}")
        if product["id"] in ids:
            raise ValueError(f"duplicate product id: {product['id']}")
        ids.add(product["id"])
        if product["actions"]:
            raise ValueError(
                f"{product['id']} exposes actions; add only a real public action with a reviewed contract"
            )
    return data


def detail_url(product: dict[str, Any], language: str) -> str:
    prefix = "https://www.quukk.com/en/products/" if language == "en" else "https://www.quukk.com/products/"
    return f"{prefix}{product['id']}.html"


def manifest(data: dict[str, Any]) -> dict[str, Any]:
    site = data["site"]
    products: list[dict[str, Any]] = []
    for product in data["products"]:
        products.append(
            {
                "id": product["id"],
                "category": product["category"],
                "name": {"zh-CN": product["name_zh"], "en": product["name_en"]},
                "aliases": product.get("aliases", []),
                "url": product["url"],
                "detail_pages": {"zh-CN": detail_url(product, "zh"), "en": detail_url(product, "en")},
                "machine_readable": {
                    "markdown_zh": detail_url(product, "zh")[:-5] + ".md",
                    "markdown_en": detail_url(product, "en")[:-5] + ".md",
                    "json_zh": detail_url(product, "zh")[:-5] + ".json",
                    "json_en": detail_url(product, "en")[:-5] + ".json",
                },
                "description": {"zh-CN": product["description_zh"], "en": product["description_en"]},
                "capabilities": product["capabilities"],
                "limits": product["limits"],
                "access": product.get("access", "external_site"),
                "actions": product["actions"],
                "status": product["status"],
                "last_verified": product["last_verified"],
                "evidence": product["evidence"],
            }
        )
    return {
        "schema_version": "1",
        "type": "agent-manifest",
        "site": {
            "name": site["name"],
            "url": site["url"],
            "languages": site["languages"],
            "description": {"zh-CN": site["description_zh"], "en": site["description_en"]},
            "contact": site["contact"],
        },
        "glossary": site["glossary"],
        "brand": site["brand"],
        "discovery": {
            "llms": "https://www.quukk.com/llms.txt",
            "llms_full": "https://www.quukk.com/llms-full.txt",
            "manifest": "https://www.quukk.com/agent-manifest.json",
            "sitemap": "https://www.quukk.com/sitemap.xml",
            "note": "llms-full.txt is a convenience export, not a standardized protocol. No public business actions are exposed by this manifest.",
        },
        "products": products,
    }


def concise_llms(data: dict[str, Any]) -> str:
    site = data["site"]
    lines = [
        "# quukk",
        "",
        f"> {site['description_zh']}",
        "",
        "## 机器可读入口",
        "",
        "- [agent-manifest.json](https://www.quukk.com/agent-manifest.json): 产品、能力、限制、状态、来源和最后核验日期。",
        "- [完整文本导出 llms-full.txt](https://www.quukk.com/llms-full.txt): 方便模型读取的完整文本；它不是正式标准。",
        "- [术语表](https://www.quukk.com/glossary.html): Agentor 与 AgentOrg 的定义。",
        "",
        "## 应用平台",
        "",
    ]
    for product in data["products"]:
        if product["category"] == "application":
            lines.append(
                f"- [{product['name_zh']}]({product['url']}): {product['description_zh']} [产品页](https://www.quukk.com/products/{product['id']}.html) [Markdown](https://www.quukk.com/products/{product['id']}.md)"
            )
    lines.extend(["", "## 支撑平台", ""])
    for product in data["products"]:
        if product["category"] == "support":
            lines.append(
                f"- [{product['name_zh']}]({product['url']}): {product['description_zh']} [产品页](https://www.quukk.com/products/{product['id']}.html) [Markdown](https://www.quukk.com/products/{product['id']}.md)"
            )
    lines.extend(
        [
            "",
            "## 内容边界",
            "",
            "- 产品条目当前记录的是公开介绍，status 为 public_description。",
            "- 页面中的界面截图可能是演示数据或界面示例，不等同于生产环境能力验收。",
            "- 本站没有在此清单中声明匿名 API、MCP 工具或可直接执行的业务动作。",
            "- 每个产品条目的 evidence 和 last_verified 字段用于追溯来源和核验时间。",
            "",
        ]
    )
    return "\n".join(lines)


def full_llms(data: dict[str, Any]) -> str:
    site = data["site"]
    lines = [
        "# quukk full machine-readable text",
        "",
        "> This is a convenience export for retrieval. It is not a standardized protocol and does not grant access to private data.",
        "",
        "## Site",
        "",
        f"- Name: {site['name']}",
        f"- URL: {site['url']}",
        f"- 中文说明: {site['description_zh']}",
        f"- English description: {site['description_en']}",
        f"- Glossary (zh): {site['glossary']['zh']}",
        f"- Glossary (en): {site['glossary']['en']}",
        "",
    ]
    for category, heading in (("application", "Application products"), ("support", "Support platforms")):
        lines.extend([f"## {heading}", ""])
        for product in data["products"]:
            if product["category"] != category:
                continue
            lines.extend(
                [
                    f"### {product['name_en']} / {product['name_zh']}",
                    "",
                    f"- ID: {product['id']}",
                    f"- Official URL: {product['url']}",
                    f"- Detail page (zh): https://www.quukk.com/products/{product['id']}.html",
                    f"- Detail page (en): https://www.quukk.com/en/products/{product['id']}.html",
                    f"- Description (zh): {product['description_zh']}",
                    f"- Description (en): {product['description_en']}",
                    f"- Access: {product.get('access', 'external_site')}",
                    f"- Status: {product['status']}",
                    f"- Last verified: {product['last_verified']}",
                    "- Capabilities:",
                ]
            )
            for capability in product["capabilities"]:
                lines.append(
                    f"  - {capability['name_zh']} / {capability['name_en']} ({capability['status']})"
                )
            lines.append("- Limits:")
            lines.extend(f"  - {limit}" for limit in product["limits"])
            lines.append("- Actions: none declared")
            lines.append("- Evidence:")
            for evidence in product["evidence"]:
                note = evidence.get("note_zh", "")
                lines.append(f"  - {evidence['kind']}: {evidence['url']} {note}".rstrip())
            lines.append("")
    lines.extend(
        [
            "## Boundaries",
            "",
            "- A public description is not a production acceptance report.",
            "- Screenshots marked as examples or demo data should be treated as illustrative.",
            "- No public business actions are declared by this export.",
            "",
        ]
    )
    return "\n".join(lines)


def product_json(product: dict[str, Any], language: str) -> dict[str, Any]:
    is_english = language == "en"
    return {
        "schema_version": "1",
        "id": product["id"],
        "category": product["category"],
        "name": product["name_en"] if is_english else product["name_zh"],
        "aliases": product.get("aliases", []),
        "description": product["description_en"] if is_english else product["description_zh"],
        "url": product["url"],
        "detail_page": detail_url(product, language),
        "capabilities": [
            {
                "id": item["id"],
                "name": item["name_en"] if is_english else item["name_zh"],
                "status": item["status"],
            }
            for item in product["capabilities"]
        ],
        "limits": product["limits"],
        "access": product.get("access", "external_site"),
        "actions": product["actions"],
        "status": product["status"],
        "last_verified": product["last_verified"],
        "evidence": product["evidence"],
    }


def product_markdown(product: dict[str, Any], language: str) -> str:
    is_english = language == "en"
    name = product["name_en"] if is_english else product["name_zh"]
    description = product["description_en"] if is_english else product["description_zh"]
    capability_lines = []
    for item in product["capabilities"]:
        capability_lines.append(
            f"- {item['name_en'] if is_english else item['name_zh']} (`{item['status']}`)"
        )
    limits = "\n".join(f"- {item}" for item in product["limits"])
    evidence = "\n".join(
        f"- `{item['kind']}`: {item['url']}"
        + (f" — {item['note_en']}" if is_english and item.get("note_en") else f" — {item['note_zh']}" if item.get("note_zh") else "")
        for item in product["evidence"]
    )
    if is_english:
        labels = {
            "description": "Description", "capabilities": "Capabilities", "limits": "Limits",
            "access": "Access", "status": "Evidence status", "verified": "Last verified",
            "official": "Official product URL", "actions": "Public actions",
        }
        actions = "None declared."
    else:
        labels = {
            "description": "说明", "capabilities": "能力", "limits": "边界", "access": "访问方式",
            "status": "证据状态", "verified": "最后核验", "official": "官方产品入口", "actions": "公开动作",
        }
        actions = "当前未声明公开动作。"
    return "\n".join(
        [
            f"# {name}",
            "",
            f"{description}",
            "",
            f"## {labels['capabilities']}",
            "",
            *capability_lines,
            "",
            f"## {labels['limits']}",
            "",
            limits,
            "",
            f"- **{labels['official']}**: {product['url']}",
            f"- **{labels['access']}**: {product.get('access', 'external_site')}",
            f"- **{labels['status']}**: {product['status']}",
            f"- **{labels['verified']}**: {product['last_verified']}",
            f"- **{labels['actions']}**: {actions}",
            "",
            f"## Evidence / 证据",
            "",
            evidence,
            "",
            ("This page records public descriptions and evidence boundaries; it is not a production acceptance report." if is_english else "本页记录公开介绍及证据边界，不是生产环境验收报告。"),
            "",
        ]
    )


def product_jsonld(product: dict[str, Any], language: str) -> dict[str, Any]:
    is_english = language == "en"
    page = detail_url(product, language)
    name = product["name_en"] if is_english else product["name_zh"]
    description = product["description_en"] if is_english else product["description_zh"]
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "SoftwareApplication",
                "@id": f"{page}#software",
                "name": name,
                "description": description,
                "url": page,
                "sameAs": product["url"],
                "applicationCategory": "AI application" if product["category"] == "application" else "AI infrastructure",
                "featureList": [item["name_en"] if is_english else item["name_zh"] for item in product["capabilities"]],
                "dateModified": product["last_verified"],
                "isPartOf": {"@id": "https://www.quukk.com/#website"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{page}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "quukk", "item": "https://www.quukk.com/en/" if is_english else "https://www.quukk.com/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": page},
                ],
            },
        ],
    }


def product_html(product: dict[str, Any], language: str) -> str:
    is_english = language == "en"
    page = detail_url(product, language)
    name = product["name_en"] if is_english else product["name_zh"]
    description = product["description_en"] if is_english else product["description_zh"]
    capabilities = "".join(
        f'<li><strong>{escape(item["name_en"] if is_english else item["name_zh"])}</strong> <span class="status">({escape(item["status"])})</span></li>'
        for item in product["capabilities"]
    )
    limits = "".join(f"<li>{escape(item)}</li>" for item in product["limits"])
    evidence = "".join(
        f'<li><code>{escape(item["kind"])}</code> · <a href="{escape(item["url"])}">{escape(item["url"])}</a>'
        + (f' · {escape(item["note_en"])}' if is_english and item.get("note_en") else f' · {escape(item["note_zh"])}' if item.get("note_zh") else "")
        + "</li>"
        for item in product["evidence"]
    )
    if is_english:
        title = f"{name} | quukk product details"
        labels = {"home": "quukk home", "other": "中文", "capabilities": "Capabilities", "limits": "Limits", "access": "Access", "status": "Evidence status", "verified": "Last verified", "evidence": "Evidence", "official": "Open official product", "actions": "Public actions", "none": "None declared", "note": "This page records public descriptions and evidence boundaries; it is not a production acceptance report."}
        other_page = detail_url(product, "zh")
    else:
        title = f"{name}｜quukk 产品说明"
        labels = {"home": "quukk 首页", "other": "EN", "capabilities": "能力", "limits": "边界", "access": "访问方式", "status": "证据状态", "verified": "最后核验", "evidence": "证据", "official": "打开官方产品入口", "actions": "公开动作", "none": "当前未声明公开动作", "note": "本页记录公开介绍及证据边界，不是生产环境验收报告。"}
        other_page = detail_url(product, "en")
    json_payload = json.dumps(product_json(product, language), ensure_ascii=False, indent=2)
    jsonld = json.dumps(product_jsonld(product, language), ensure_ascii=False, indent=2)
    return f'''<!doctype html>
<html lang="{'en' if is_english else 'zh-CN'}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{page}">
  <link rel="alternate" hreflang="zh-CN" href="{detail_url(product, 'zh')}">
  <link rel="alternate" hreflang="en" href="{detail_url(product, 'en')}">
  <link rel="alternate" hreflang="x-default" href="{detail_url(product, 'zh')}">
  <link rel="alternate" type="text/markdown" href="{page[:-5]}.md">
  <link rel="alternate" type="application/json" href="{page[:-5]}.json">
  <script type="application/ld+json">{jsonld}</script>
  <style>
    :root {{ color-scheme: light; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #382c24; background: #faf7f2; }}
    body {{ max-width: 880px; margin: 0 auto; padding: 32px 22px 64px; line-height: 1.7; }}
    a {{ color: #8b482e; }}
    header {{ border-bottom: 1px solid #ddcdbd; margin-bottom: 36px; padding-bottom: 18px; }}
    nav {{ display: flex; flex-wrap: wrap; gap: 16px; font-size: .95rem; }}
    h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); line-height: 1.1; margin: 20px 0 12px; }}
    h2 {{ margin-top: 34px; font-size: 1.45rem; }}
    .lede {{ font-size: 1.15rem; max-width: 68ch; }}
    .meta {{ background: #f1e7dc; border-radius: 8px; padding: 18px 20px; }}
    .meta dt {{ font-weight: 700; }}
    .meta dd {{ margin: 0 0 8px; }}
    .status {{ color: #756454; font-size: .9em; }}
    code {{ font-size: .9em; }}
    footer {{ border-top: 1px solid #ddcdbd; margin-top: 48px; padding-top: 18px; font-size: .92rem; color: #756454; }}
  </style>
</head>
<body>
  <header>
    <nav aria-label="{escape(labels['home'])}"><a href="{'/en/' if is_english else '/'}">{escape(labels['home'])}</a><a href="{escape(other_page)}" lang="{'zh-CN' if is_english else 'en'}">{escape(labels['other'])}</a><a href="/agent-manifest.json">agent-manifest.json</a><a href="/llms.txt">llms.txt</a></nav>
    <h1>{escape(name)}</h1>
    <p class="lede">{escape(description)}</p>
  </header>
  <main>
    <section aria-labelledby="capabilities-title"><h2 id="capabilities-title">{escape(labels['capabilities'])}</h2><ul>{capabilities}</ul></section>
    <section aria-labelledby="limits-title"><h2 id="limits-title">{escape(labels['limits'])}</h2><ul>{limits}</ul></section>
    <section aria-labelledby="metadata-title"><h2 id="metadata-title">{escape(labels['status'])}</h2><dl class="meta"><dt>{escape(labels['official'])}</dt><dd><a href="{escape(product['url'])}">{escape(product['url'])}</a></dd><dt>{escape(labels['access'])}</dt><dd>{escape(product.get('access', 'external_site'))}</dd><dt>{escape(labels['status'])}</dt><dd>{escape(product['status'])}</dd><dt>{escape(labels['verified'])}</dt><dd>{escape(product['last_verified'])}</dd><dt>{escape(labels['actions'])}</dt><dd>{escape(labels['none'])}</dd></dl></section>
    <section aria-labelledby="evidence-title"><h2 id="evidence-title">{escape(labels['evidence'])}</h2><ul>{evidence}</ul><p>{escape(labels['note'])}</p></section>
  </main>
  <footer><a href="{page[:-5]}.md">Markdown</a> · <a href="{page[:-5]}.json">JSON</a> · <a href="/sitemap.xml">sitemap.xml</a></footer>
</body>
</html>
'''


def write_product_derivatives(data: dict[str, Any]) -> None:
    for language in ("zh", "en"):
        directory = DIST / ("en/products" if language == "en" else "products")
        directory.mkdir(parents=True, exist_ok=True)
        for product in data["products"]:
            stem = directory / product["id"]
            write(stem.with_suffix(".html"), product_html(product, language))
            write(stem.with_suffix(".md"), product_markdown(product, language))
            write(stem.with_suffix(".json"), json.dumps(product_json(product, language), ensure_ascii=False, indent=2) + "\n")


def write_sitemap(data: dict[str, Any]) -> None:
    root = ET.Element(f"{{{SM_NS}}}urlset")

    def add_pair(zh_path: str, en_path: str, lastmod: str) -> None:
        for path, default in ((zh_path, zh_path), (en_path, zh_path)):
            url = ET.SubElement(root, f"{{{SM_NS}}}url")
            ET.SubElement(url, f"{{{SM_NS}}}loc").text = f"https://www.quukk.com{path}"
            ET.SubElement(url, f"{{{SM_NS}}}lastmod").text = lastmod
            for hreflang, href in (("zh-CN", zh_path), ("en", en_path), ("x-default", zh_path)):
                link = ET.SubElement(url, f"{{{XHTML_NS}}}link", {
                    "rel": "alternate",
                    "hreflang": hreflang,
                    "href": f"https://www.quukk.com{href}",
                })

    add_pair("/", "/en/", "2026-11-14")
    add_pair("/glossary.html", "/en/glossary.html", "2026-11-14")
    add_pair("/brand.html", "/en/brand.html", "2026-11-08")
    for product in data["products"]:
        add_pair(f"/products/{product['id']}.html", f"/en/products/{product['id']}.html", product["last_verified"])

    if hasattr(ET, "indent"):
        ET.indent(root, space="  ")
    write(DIST / "sitemap.xml", ET.tostring(root, encoding="unicode", xml_declaration=True))


def update_homepage_jsonld(data: dict[str, Any]) -> None:
    """Keep the homepage entity graph aligned with the product source of truth."""
    for relative, language in (("index.html", "zh"), ("en/index.html", "en")):
        path = DIST / relative
        text = path.read_text(encoding="utf-8")
        match = re.search(r'(<script type="application/ld\+json">\n)(.*?)(\n  </script>)', text, re.S)
        if not match:
            raise ValueError(f"missing homepage JSON-LD block: {relative}")
        payload = json.loads(match.group(2))
        graph = payload.get("@graph", [])
        homepage = "https://www.quukk.com/en/" if language == "en" else "https://www.quukk.com/"
        webpage = next((node for node in graph if node.get("@type") == "CollectionPage"), None)
        if webpage is not None:
            webpage["dateModified"] = "2026-11-14"
            webpage["hasPart"] = [
                {"@id": f"https://www.quukk.com/{'en/' if language == 'en' else ''}products/{p['id']}.html#software"}
                for p in data["products"]
            ]
        item_list = next((node for node in graph if node.get("@type") == "ItemList" and node.get("@id", "").endswith("product-list")), None)
        app_products = [p for p in data["products"] if p["category"] == "application"]
        if item_list is not None:
            item_list["numberOfItems"] = len(app_products)
            item_list["itemListElement"] = [
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": p["name_en"] if language == "en" else p["name_zh"],
                    "url": f"https://www.quukk.com/{'en/' if language == 'en' else ''}products/{p['id']}.html",
                }
                for index, p in enumerate(app_products, 1)
            ]
        breadcrumb_id = f"{homepage}#breadcrumb"
        if not any(node.get("@id") == breadcrumb_id for node in graph):
            graph.append(
                {
                    "@type": "BreadcrumbList",
                    "@id": breadcrumb_id,
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "name": "quukk",
                            "item": homepage,
                        }
                    ],
                }
            )
        support_id = f"{homepage}#support-list"
        if not any(node.get("@id") == support_id for node in graph):
            support_products = [p for p in data["products"] if p["category"] == "support"]
            graph.append(
                {
                    "@type": "ItemList",
                    "@id": support_id,
                    "name": "Support platforms" if language == "en" else "支撑平台",
                    "numberOfItems": len(support_products),
                    "itemListElement": [
                        {
                            "@type": "ListItem",
                            "position": index,
                            "name": p["name_en"] if language == "en" else p["name_zh"],
                            "url": f"https://www.quukk.com/{'en/' if language == 'en' else ''}products/{p['id']}.html",
                        }
                        for index, p in enumerate(support_products, 1)
                    ],
                }
            )
        for product in data["products"]:
            detail = f"https://www.quukk.com/{'en/' if language == 'en' else ''}products/{product['id']}.html"
            entity_id = detail + "#software"
            if any(node.get("@id") == entity_id for node in graph):
                continue
            graph.append(
                {
                    "@type": "SoftwareApplication",
                    "@id": entity_id,
                    "name": product["name_en"] if language == "en" else product["name_zh"],
                    "alternateName": product.get("aliases", []),
                    "description": product["description_en"] if language == "en" else product["description_zh"],
                    "url": detail,
                    "sameAs": product["url"],
                    "applicationCategory": "AI application" if product["category"] == "application" else "AI infrastructure",
                    "featureList": [item["name_en"] if language == "en" else item["name_zh"] for item in product["capabilities"]],
                    "dateModified": product["last_verified"],
                    "isPartOf": {"@id": f"{homepage}#website"},
                }
            )
        payload["@graph"] = graph
        replacement = json.dumps(payload, ensure_ascii=False, indent=2)
        path.write_text(text[:match.start(2)] + replacement + text[match.end(2):], encoding="utf-8")


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    data = load_source()
    write(DIST / "agent-manifest.json", json.dumps(manifest(data), ensure_ascii=False, indent=2) + "\n")
    write(DIST / "llms.txt", concise_llms(data))
    write(DIST / "llms-full.txt", full_llms(data))
    write_product_derivatives(data)
    write_sitemap(data)
    update_homepage_jsonld(data)


if __name__ == "__main__":
    main()
