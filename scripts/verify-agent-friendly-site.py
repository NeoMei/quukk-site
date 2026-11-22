#!/usr/bin/env python3
"""Validate the public machine-readable and agent-facing site surface.

This is intentionally dependency-free so it can run in the static-site checkout
before deployment. It validates the source product catalog, generated assets,
HTML detail pages, JSON-LD presence, sitemap coverage, and stale copy.
"""
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SOURCE = ROOT / "data" / "agent-products.json"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def is_url(value: object, *, http_only: bool = False) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    allowed = {"http", "https"} if http_only else {"http", "https", "mailto"}
    return parsed.scheme in allowed and bool(parsed.netloc) if parsed.scheme != "mailto" else bool(parsed.path)


def load_json(path: Path, errors: list[str]):
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}", errors)
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic branch
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}", errors)
        return None


def check_source(errors: list[str]):
    data = load_json(SOURCE, errors)
    if not isinstance(data, dict):
        return None, {}
    products = data.get("products")
    if not isinstance(products, list) or not products:
        fail("source catalog must contain a non-empty products array", errors)
        return data, {}
    by_id: dict[str, dict] = {}
    required = {
        "id", "name_zh", "name_en", "url", "description_zh", "description_en",
        "capabilities", "limits", "status", "last_verified", "evidence", "actions",
    }
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            fail(f"source product #{index + 1} is not an object", errors)
            continue
        missing = sorted(required - product.keys())
        if missing:
            fail(f"source product #{index + 1} missing keys: {', '.join(missing)}", errors)
        product_id = product.get("id")
        if not isinstance(product_id, str) or not re.fullmatch(r"[a-z0-9-]+", product_id):
            fail(f"source product #{index + 1} has invalid id: {product_id!r}", errors)
            continue
        if product_id in by_id:
            fail(f"duplicate source product id: {product_id}", errors)
        by_id[product_id] = product
        for key in ("capabilities", "limits", "evidence", "actions"):
            if key in product and not isinstance(product[key], list):
                fail(f"{product_id}.{key} must be an array", errors)
        for key in ("url",):
            if key in product and not is_url(product[key], http_only=True):
                fail(f"{product_id}.{key} must be an http(s) URL", errors)
        for key in ("name_zh", "name_en", "description_zh", "description_en", "status", "last_verified"):
            if key in product and (not isinstance(product[key], str) or not product[key].strip()):
                fail(f"{product_id}.{key} must be a non-empty string", errors)
        for evidence_index, evidence in enumerate(product.get("evidence", [])):
            if not isinstance(evidence, dict):
                fail(f"{product_id}.evidence[{evidence_index}] must be an object", errors)
                continue
            if not is_url(evidence.get("url"), http_only=True):
                fail(f"{product_id}.evidence[{evidence_index}] must include an http(s) url", errors)
    return data, by_id


def check_manifest(source_by_id: dict[str, dict], errors: list[str]):
    manifest = load_json(DIST / "agent-manifest.json", errors)
    if not isinstance(manifest, dict):
        return
    products = manifest.get("products")
    if not isinstance(products, list):
        fail("agent-manifest.json must contain a products array", errors)
        return
    manifest_by_id = {p.get("id"): p for p in products if isinstance(p, dict)}
    if set(manifest_by_id) != set(source_by_id):
        fail("manifest product ids do not match source catalog", errors)
    for product_id, source in source_by_id.items():
        item = manifest_by_id.get(product_id)
        if not item:
            continue
        manifest_values = {
            "name_zh": item.get("name", {}).get("zh-CN") if isinstance(item.get("name"), dict) else item.get("name_zh"),
            "name_en": item.get("name", {}).get("en") if isinstance(item.get("name"), dict) else item.get("name_en"),
            "url": item.get("url"),
            "status": item.get("status"),
            "last_verified": item.get("last_verified"),
        }
        for key, value in manifest_values.items():
            if value != source.get(key):
                fail(f"manifest {product_id}.{key} differs from source catalog", errors)
        if not isinstance(item.get("actions"), list):
            fail(f"manifest {product_id}.actions must be an array", errors)
        machine = item.get("machine_readable")
        if not isinstance(machine, dict) or not all(is_url(value, http_only=True) for value in machine.values()):
            fail(f"manifest {product_id}.machine_readable must contain http(s) URLs", errors)


def check_discovery_files(errors: list[str]) -> None:
    for filename in ("llms.txt", "llms-full.txt"):
        path = DIST / filename
        if not path.is_file() or not path.read_text(encoding="utf-8").lstrip().startswith("# "):
            fail(f"{filename} must exist and start with an H1", errors)
    manifest_text = (DIST / "agent-manifest.json").read_text(encoding="utf-8") if (DIST / "agent-manifest.json").is_file() else ""
    if "MCP" in manifest_text and '"actions": []' not in manifest_text:
        # Keep this as a warning-like failure only when the manifest claims actions
        # without an explicit public endpoint description.
        try:
            manifest = json.loads(manifest_text)
            for product in manifest.get("products", []):
                if product.get("actions") and not product.get("action_policy"):
                    fail(f"{product.get('id')}: actions require an explicit action_policy", errors)
        except json.JSONDecodeError:
            pass


def check_detail_pages(source_by_id: dict[str, dict], errors: list[str]) -> None:
    for product_id, source in source_by_id.items():
        for language, directory in (("zh", DIST / "products"), ("en", DIST / "en" / "products")):
            html_path = directory / f"{product_id}.html"
            md_path = directory / f"{product_id}.md"
            json_path = directory / f"{product_id}.json"
            for path in (html_path, md_path, json_path):
                if not path.is_file():
                    fail(f"missing {language} product derivative: {path.relative_to(ROOT)}", errors)
            if html_path.is_file():
                html = html_path.read_text(encoding="utf-8")
                if len(re.findall(r"<h1\b", html, re.I)) != 1:
                    fail(f"{html_path.relative_to(ROOT)} must contain exactly one h1", errors)
                if "application/ld+json" not in html:
                    fail(f"{html_path.relative_to(ROOT)} missing JSON-LD", errors)
                for needle in (source.get("status", ""), source.get("last_verified", "")):
                    if needle and needle not in html:
                        fail(f"{html_path.relative_to(ROOT)} missing visible value: {needle}", errors)
                if 'type="text/markdown"' not in html:
                    fail(f"{html_path.relative_to(ROOT)} missing Markdown alternate link", errors)
                try:
                    scripts = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
                    if not scripts:
                        fail(f"{html_path.relative_to(ROOT)} missing parseable JSON-LD block", errors)
                    else:
                        json.loads(scripts[0])
                except json.JSONDecodeError as exc:
                    fail(f"{html_path.relative_to(ROOT)} has invalid JSON-LD: {exc}", errors)
            if json_path.is_file():
                payload = load_json(json_path, errors)
                if isinstance(payload, dict):
                    for key in ("id", "name", "description", "url", "status", "last_verified"):
                        if key not in payload:
                            fail(f"{json_path.relative_to(ROOT)} missing key: {key}", errors)


def check_sitemap(source_by_id: dict[str, dict], errors: list[str]) -> None:
    path = DIST / "sitemap.xml"
    if not path.is_file():
        fail("missing dist/sitemap.xml", errors)
        return
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid sitemap.xml: {exc}", errors)
        return
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {node.text for node in root.findall("sm:url/sm:loc", ns) if node.text}
    if "https://www.quukk.com/sitemap.xml" not in (DIST / "robots.txt").read_text(encoding="utf-8"):
        fail("robots.txt must declare the canonical sitemap", errors)
    for product_id in source_by_id:
        for path_part in (f"/products/{product_id}.html", f"/en/products/{product_id}.html"):
            expected = f"https://www.quukk.com{path_part}"
            if expected not in locs:
                fail(f"sitemap missing {expected}", errors)
    for loc in locs:
        parsed = urlparse(loc)
        if parsed.netloc != "www.quukk.com":
            continue
        local = DIST / parsed.path.lstrip("/")
        if parsed.path.endswith("/"):
            local = local / "index.html"
        if not local.is_file():
            fail(f"sitemap points at missing local page: {parsed.path}", errors)


def check_homepages(errors: list[str]) -> None:
    for filename in ("index.html", "en/index.html", "glossary.html", "en/glossary.html"):
        path = DIST / filename
        if not path.is_file():
            fail(f"missing page: dist/{filename}", errors)
            continue
        text = path.read_text(encoding="utf-8")
        if "四款工具" in text or "four tools" in text.lower():
            fail(f"stale four-product copy remains in dist/{filename}", errors)
        if "application/ld+json" not in text:
            fail(f"dist/{filename} missing JSON-LD", errors)
        if 'href="/agent-manifest.json"' not in text or 'href="/llms.txt"' not in text:
            fail(f"dist/{filename} missing agent discovery links", errors)
        scripts = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', text, re.S)
        try:
            payload = json.loads(scripts[0])
            graph = payload.get("@graph", []) if isinstance(payload, dict) else []
            if filename in ("index.html", "en/index.html"):
                software_count = sum(1 for node in graph if isinstance(node, dict) and node.get("@type") == "SoftwareApplication")
                if software_count != 7:
                    fail(f"dist/{filename} must expose 7 SoftwareApplication entities, found {software_count}", errors)
                if not any(isinstance(node, dict) and node.get("@type") == "BreadcrumbList" for node in graph):
                    fail(f"dist/{filename} missing BreadcrumbList JSON-LD", errors)
        except (IndexError, json.JSONDecodeError) as exc:
            fail(f"dist/{filename} has invalid JSON-LD: {exc}", errors)


def main() -> int:
    errors: list[str] = []
    _, source_by_id = check_source(errors)
    check_manifest(source_by_id, errors)
    check_discovery_files(errors)
    check_detail_pages(source_by_id, errors)
    check_sitemap(source_by_id, errors)
    check_homepages(errors)
    if errors:
        print("agent-friendly site verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"agent-friendly site verification passed: {len(source_by_id)} products checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
