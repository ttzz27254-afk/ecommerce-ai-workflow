# ecommerce-ai-workflow

This repository contains a Codex skill for ecommerce operators who need help with:

- automated listing/upload-sheet preparation;
- competitor data organization and analysis;
- competitor image parsing;
- compliant image-generation prompt planning.

## Skill

Use the skill in `ecommerce-operator-ai/` when preparing ecommerce launch files or competitor reports. The skill includes CSV templates, operator references, and a Python script that generates a starter operations pack.

Quick test command:

```bash
python ecommerce-operator-ai/scripts/ecommerce_ops_pack.py \
  --products ecommerce-operator-ai/assets/product_brief_template.csv \
  --competitors ecommerce-operator-ai/assets/competitor_links_template.csv \
  --out-dir /tmp/ecommerce_ops_pack_test \
  --platform Amazon \
  --market US
```
