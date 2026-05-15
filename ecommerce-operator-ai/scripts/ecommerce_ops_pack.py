#!/usr/bin/env python3
"""Generate a starter ecommerce operations pack from simple CSV inputs.

This script intentionally uses only the Python standard library so a non-technical
operator can run it in most environments without installing dependencies.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


PRODUCT_FIELDS = [
    "sku",
    "product_name",
    "brand",
    "category",
    "variant",
    "material",
    "color",
    "size",
    "package_contents",
    "target_customer",
    "core_benefit",
    "feature_1",
    "feature_2",
    "feature_3",
    "proof_points",
    "price",
    "cost",
    "inventory",
    "keywords",
    "compliance_notes",
    "image_notes",
]

LISTING_FIELDS = [
    "sku",
    "platform",
    "market",
    "title",
    "brand",
    "category",
    "variant",
    "price",
    "inventory",
    "bullet_1",
    "bullet_2",
    "bullet_3",
    "bullet_4",
    "bullet_5",
    "description",
    "search_terms",
    "image_plan",
    "compliance_flags",
]

IMAGE_FIELDS = [
    "sku",
    "image_role",
    "prompt",
    "negative_prompt",
    "ratio",
    "qa_notes",
]

RISK_WORDS = [
    "waterproof",
    "medical",
    "fda",
    "cure",
    "guaranteed",
    "best",
    "no.1",
    "patented",
    "organic",
    "child-safe",
    "food-safe",
]


@dataclass
class Product:
    row: dict[str, str]

    def get(self, key: str, default: str = "") -> str:
        return clean(self.row.get(key, default))

    @property
    def sku(self) -> str:
        return self.get("sku") or slugify(self.get("product_name"))[:24] or "SKU-DRAFT"


@dataclass
class Competitor:
    row: dict[str, str]

    def get(self, key: str, default: str = "") -> str:
        return clean(self.row.get(key, default))


def clean(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def slugify(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").upper()
    return text or "DRAFT"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def split_keywords(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,;，；|]", text) if item.strip()]


def format_price(value: str) -> str:
    try:
        return f"{float(value):.2f}"
    except ValueError:
        return value


def build_title(product: Product) -> str:
    brand = product.get("brand")
    name = product.get("product_name")
    keywords = split_keywords(product.get("keywords"))
    core_keyword = keywords[0] if keywords else product.get("category")
    differentiator = product.get("feature_1") or product.get("core_benefit")
    variant_parts = ", ".join(part for part in [product.get("color"), product.get("size"), product.get("variant")] if part)
    title_parts = [brand, core_keyword or name, differentiator, "for " + product.get("target_customer") if product.get("target_customer") else "", variant_parts]
    title = " - ".join(part for part in title_parts if part)
    return title[:190]


def risk_flags(product: Product) -> str:
    combined = " ".join(product.get(field) for field in PRODUCT_FIELDS).lower()
    hits = [word for word in RISK_WORDS if word in combined]
    notes = product.get("compliance_notes")
    if hits and notes:
        return f"Check proof for: {', '.join(sorted(set(hits)))}. Notes: {notes}"
    if hits:
        return f"Check proof for: {', '.join(sorted(set(hits)))}"
    return notes or "No obvious claim flags found; still review platform policy."


def listing_row(product: Product, platform: str, market: str) -> dict[str, str]:
    feature_1 = product.get("feature_1")
    feature_2 = product.get("feature_2")
    feature_3 = product.get("feature_3")
    benefit = product.get("core_benefit")
    proof = product.get("proof_points")
    package = product.get("package_contents")
    material_size = ", ".join(part for part in [product.get("material"), product.get("size")] if part)
    description = (
        f"{product.get('product_name')} is designed for {product.get('target_customer') or 'everyday customers'} "
        f"who need {benefit or 'a practical and reliable solution'}. "
        f"Key details: {material_size or 'confirm material and size'}. "
        f"Package contents: {package or 'confirm package contents'}. "
        f"Use the product as shown in the final approved images and follow all care instructions."
    )
    return {
        "sku": product.sku,
        "platform": platform,
        "market": market,
        "title": build_title(product),
        "brand": product.get("brand"),
        "category": product.get("category"),
        "variant": product.get("variant") or product.get("color") or product.get("size"),
        "price": format_price(product.get("price")),
        "inventory": product.get("inventory"),
        "bullet_1": f"Organized for daily use: {benefit}" if benefit else "Draft benefit bullet: confirm the main customer problem solved.",
        "bullet_2": f"Built with practical details: {feature_1}" if feature_1 else "Draft differentiator bullet: add the strongest feature.",
        "bullet_3": f"Designed for real scenarios: {feature_2}" if feature_2 else "Draft use-case bullet: add where customers use it.",
        "bullet_4": f"Helpful product details: {feature_3 or material_size or 'confirm specifications'}",
        "bullet_5": f"What you receive: {package}. Proof/details: {proof}" if package or proof else "Draft trust bullet: add package contents, warranty, or service promise if true.",
        "description": description,
        "search_terms": ", ".join(split_keywords(product.get("keywords"))[:20]),
        "image_plan": "Hero image; lifestyle use scene; feature callout; size comparison; package contents; usage/care steps.",
        "compliance_flags": risk_flags(product),
    }


def image_rows(product: Product) -> list[dict[str, str]]:
    base = f"Product: {product.get('product_name')} ({product.get('color')} {product.get('material')}). Core benefit: {product.get('core_benefit')}."
    negative = "no competitor logo, no fake certification, no false review stars, no unreadable text, no distorted product, no extra accessories not included, no watermark"
    prompts = [
        ("main_hero", f"{base} Clean marketplace hero image on a simple light background, accurate product shape and color, soft studio lighting, centered composition, no text.", "1:1"),
        ("lifestyle", f"{base} Realistic lifestyle scene for {product.get('target_customer') or 'the target customer'}, showing the product in normal use with natural lighting and uncluttered props.", "4:5"),
        ("feature_callout", f"{base} Original infographic-style feature callout highlighting {product.get('feature_1') or 'the main feature'}, simple brand-color labels, factual text only.", "1:1"),
        ("package_contents", f"{base} Neatly arranged package contents: {product.get('package_contents') or 'confirm included items'}, clean background, accurate scale.", "1:1"),
    ]
    return [
        {
            "sku": product.sku,
            "image_role": role,
            "prompt": prompt,
            "negative_prompt": negative,
            "ratio": ratio,
            "qa_notes": "Confirm image matches real SKU, variant, dimensions, included items, and platform policy before publishing.",
        }
        for role, prompt, ratio in prompts
    ]


def competitor_markdown(competitors: list[Competitor], products: list[Product], platform: str, market: str) -> str:
    prices: list[float] = []
    for comp in competitors:
        try:
            prices.append(float(comp.get("price")))
        except ValueError:
            pass
    avg_price = f"{mean(prices):.2f}" if prices else "N/A"
    lines = [
        f"# Competitor Analysis Draft ({platform}, {market})",
        "",
        "## Executive Summary",
        "",
        f"- Products reviewed: {len(products)}.",
        f"- Competitors reviewed: {len(competitors)}.",
        f"- Average competitor price from usable rows: {avg_price}.",
        "- Treat this as a draft: verify live prices, claims, reviews, and images before decisions.",
        "",
        "## Competitor Table",
        "",
        "| Competitor | Platform | Price | Rating | Reviews | Main claims | Strengths | Weaknesses | Image strategy | URL |",
        "| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for comp in competitors:
        strengths = comp.get("top_features") or "Needs manual review"
        weaknesses = comp.get("weaknesses") or "Needs review mining"
        lines.append(
            "| {name} | {platform} | {price} | {rating} | {reviews} | {claims} | {strengths} | {weaknesses} | {image} | {url} |".format(
                name=comp.get("competitor_name") or "Unnamed",
                platform=comp.get("platform") or platform,
                price=comp.get("price") or "N/A",
                rating=comp.get("rating") or "N/A",
                reviews=comp.get("review_count") or "N/A",
                claims=comp.get("main_claims") or "N/A",
                strengths=strengths,
                weaknesses=weaknesses,
                image=comp.get("image_strategy") or "Needs image parsing",
                url=comp.get("url") or "N/A",
            )
        )
    lines.extend(
        [
            "",
            "## Opportunity Map",
            "",
            "| Gap | Recommendation | Priority | Evidence needed |",
            "| --- | --- | --- | --- |",
            "| Content | Rewrite title/bullets around the strongest customer benefit and missing competitor keywords. | High | Confirm keyword list and platform limits. |",
            "| Product | Match must-have features, then emphasize real differentiators. | High | Supplier specs and sample inspection. |",
            "| Image | Build original hero, lifestyle, feature, size, package, and usage images. | High | Real product photos and brand direction. |",
            "| Reviews | Mine repeated praise/complaints before final positioning. | Medium | Export or summarize top reviews. |",
            "",
            "## Next Actions",
            "",
            "1. Replace sample competitor rows with real URLs and metrics.",
            "2. Verify risky claims and certifications before using them in listings or images.",
            "3. Use `image_briefs.csv` to create original images, not copies of competitor assets.",
            "4. Finalize price after margin, ads cost, shipping, and competitor pressure review.",
        ]
    )
    return "\n".join(lines) + "\n"


def checklist_markdown(products: list[Product], platform: str, market: str) -> str:
    product_list = "\n".join(f"- {product.sku}: {product.get('product_name')}" for product in products)
    return f"""# Launch Checklist ({platform}, {market})

## Products

{product_list or '- No product rows found.'}

## Before Upload

- [ ] All required platform fields are filled.
- [ ] SKU, variant, price, inventory, package contents, and images match.
- [ ] Title and bullets do not contain unsupported claims.
- [ ] Certifications, safety claims, waterproof/medical/organic claims have proof.
- [ ] Search terms avoid irrelevant or unauthorized competitor trademarks.
- [ ] Main image follows platform requirements.
- [ ] Lifestyle and feature images are original and do not copy competitor IP.
- [ ] Shipping dimensions, weight, and return policy are confirmed.

## Missing Information to Confirm

- [ ] Final platform category.
- [ ] Final keyword list.
- [ ] Real product dimensions and material proof.
- [ ] Brand color and image style.
- [ ] Review-mining evidence from competitors.
"""


def build_pack(products_path: Path, competitors_path: Path, out_dir: Path, platform: str, market: str) -> None:
    product_rows = read_csv(products_path)
    competitor_rows = read_csv(competitors_path) if competitors_path.exists() else []
    products = [Product(row) for row in product_rows]
    competitors = [Competitor(row) for row in competitor_rows]
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "listings.csv", LISTING_FIELDS, (listing_row(product, platform, market) for product in products))
    image_data = [row for product in products for row in image_rows(product)]
    write_csv(out_dir / "image_briefs.csv", IMAGE_FIELDS, image_data)
    (out_dir / "competitor_analysis.md").write_text(competitor_markdown(competitors, products, platform, market), encoding="utf-8")
    (out_dir / "launch_checklist.md").write_text(checklist_markdown(products, platform, market), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ecommerce listing, competitor, image, and launch draft files from CSV templates.")
    parser.add_argument("--products", required=True, type=Path, help="Path to product CSV using product_brief_template.csv headers.")
    parser.add_argument("--competitors", required=True, type=Path, help="Path to competitor CSV using competitor_links_template.csv headers.")
    parser.add_argument("--out-dir", required=True, type=Path, help="Output folder for generated files.")
    parser.add_argument("--platform", default="Amazon", help="Target platform name, e.g. Amazon, Shopify, TikTok Shop.")
    parser.add_argument("--market", default="US", help="Target market/country/language, e.g. US, UK, DE, JP.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.products.exists():
        raise SystemExit(f"Product CSV not found: {args.products}")
    if not args.competitors.exists():
        raise SystemExit(f"Competitor CSV not found: {args.competitors}")
    build_pack(args.products, args.competitors, args.out_dir, args.platform, args.market)
    print(f"Generated ecommerce operations pack in: {os.fspath(args.out_dir)}")


if __name__ == "__main__":
    main()
