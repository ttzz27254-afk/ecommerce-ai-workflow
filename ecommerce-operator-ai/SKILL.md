---
name: ecommerce-operator-ai
description: End-to-end ecommerce operations workflow for non-technical sellers and operators. Use when Codex needs to help with automated product listing/upload links, marketplace listing sheets, product title/bullet/description generation, competitor link collection, competitor data analysis, price/feature/review positioning, competitor image parsing, image-generation prompts, image QA, and operational reports for platforms such as Amazon, Shopify, TikTok Shop, Temu, Shein, Shopee, Lazada, Etsy, eBay, Walmart Marketplace, or independent stores.
---

# Ecommerce Operator AI

## Outcome

Use this skill to turn an operator's raw product information, competitor links/files, images, and goals into ready-to-use ecommerce deliverables:

- Marketplace upload/listing tables.
- SEO titles, selling points, descriptions, attributes, tags, and FAQ copy.
- Competitor data-cleaning, scoring, positioning, and action recommendations.
- Competitor image parsing reports and compliant image-generation briefs/prompts.
- Launch QA checklists and daily/weekly operation summaries.

Treat the user as non-technical. Ask for missing business inputs in plain language, but never require the user to understand code.

## Quick Start Decision Tree

1. **User has product data and wants listings**: use `references/marketplace_field_map.md`, then generate a listing sheet. If local files are present, run `scripts/ecommerce_ops_pack.py`.
2. **User has competitor links/data and wants analysis**: use `references/competitor_analysis_framework.md`; run the script if CSV/XLSX-exported-as-CSV data exists.
3. **User has competitor images or wants new images**: use `references/image_workflow.md`; create image parsing notes, generation prompts, negative prompts, and QA rules.
4. **User wants a complete workflow**: produce the four-file pack: `listings.csv`, `competitor_analysis.md`, `image_briefs.csv`, and `launch_checklist.md`.

## Required Inputs to Request

Ask only for what is missing:

- Platform(s): Amazon, Shopify, TikTok Shop, Shopee, etc.
- Product basics: product name, brand, category, variants, materials/specs, package contents, target customer, price/cost, inventory, shipping limits.
- Compliance constraints: prohibited claims, certifications, regulated category limits, trademarks, image-rights restrictions.
- Competitor evidence: URLs, exported CSV, screenshots, prices, ratings, review counts, images.
- Brand direction: tone, color palette, forbidden words, value proposition.
- Output language and market: e.g., US English, German, Japanese, Simplified Chinese.

If the user provides too little information, create a clearly marked draft and a short “请补充” list.

## Standard Workflow

### 1. Intake and Normalize

- Convert messy notes into a structured product brief.
- Deduplicate competitor links by canonical URL and seller/product identity.
- Separate facts from assumptions. Mark assumptions as `待确认` in Chinese outputs or `Needs confirmation` in English outputs.
- Do not fabricate certifications, clinical claims, review counts, sales figures, platform rankings, or legal guarantees.

### 2. Listing Generation

Use the marketplace field map to create:

- SEO title with core keyword near the front.
- 5 bullet points focused on benefit, proof, use case, differentiator, and risk reversal.
- Short description and long description.
- Search terms/tags without competitor trademarks unless the platform and brand owner permit it.
- Variant names and SKU naming recommendations.
- Upload-ready table headers for the target platform.

### 3. Competitor Analysis

Score competitors on:

- Price band and promo strategy.
- Main selling points and feature gaps.
- Image/video strategy.
- Review themes: purchase drivers, complaints, quality issues, unmet needs.
- Shipping/returns/service promises.
- Content quality and keyword coverage.

Output a concise decision table: `跟进动作`, `优先级`, `影响`, `所需资料`, `负责人/下一步`.

### 4. Image Parsing and Generation

When analyzing competitor images:

- Describe layout, camera angle, background, props, color, typography, claims, scene, and information hierarchy.
- Extract reusable strategy, not copyrighted expression. Do not ask to copy a competitor image exactly.
- Identify compliance risks: medical claims, before/after claims, unverifiable badges, misleading scale, trademark/logo exposure.

When generating new image prompts:

- Create prompts for hero image, lifestyle scene, feature callout, size comparison, usage steps, package contents, and social ad variants.
- Include negative prompts: no competitor logos, no fake certifications, no misleading claims, no distorted product, no unreadable text.
- Specify output ratio and platform constraints.

### 5. QA and Launch

Before final delivery, check:

- Title length, banned words, duplicate keywords, unsupported claims.
- Variant consistency and SKU uniqueness.
- Price/feature consistency across table, copy, and images.
- Image prompt compliance and rights safety.
- Missing fields that may block publishing.

## Bundled Resources

- `scripts/ecommerce_ops_pack.py`: Generate a starter operations pack from product and competitor CSV files using only Python standard library.
- `assets/product_brief_template.csv`: Simple product data template for non-technical users.
- `assets/competitor_links_template.csv`: Competitor research template.
- `references/marketplace_field_map.md`: Platform upload fields and copy rules.
- `references/competitor_analysis_framework.md`: Competitor scoring and report framework.
- `references/image_workflow.md`: Image parsing and generation prompt workflow.
- `references/operator_checklists.md`: Plain-language intake and launch checklists.

## Script Usage

Run from the skill folder or pass paths explicitly:

```bash
python scripts/ecommerce_ops_pack.py \
  --products assets/product_brief_template.csv \
  --competitors assets/competitor_links_template.csv \
  --out-dir output/demo_pack \
  --market "US" \
  --platform "Amazon"
```

The script writes:

- `listings.csv`
- `competitor_analysis.md`
- `image_briefs.csv`
- `launch_checklist.md`

Use script output as a draft, then refine with platform rules and user-provided facts.

## Tone for Non-Technical Operators

- Prefer short tables and checklists.
- Explain what the user should upload or copy/paste.
- Avoid implementation jargon unless the user asks.
- Provide exact filenames and next actions.
- In Chinese, use practical ecommerce language: `主图`, `卖点图`, `详情页`, `竞品`, `上架表`, `转化率`, `差异化`, `合规风险`.
