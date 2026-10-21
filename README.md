# EquipQuote

**Industrial equipment quotation generator for SME B2B sales engineers — with China VAT calculation and RMB amount-in-words (人民币大写).**

Field sales engineers in small and mid-sized equipment companies still build
quotations by hand in spreadsheets: totals drift, tax is re-typed, and the
legally required Chinese uppercase amount on a quotation is easy to get wrong.
EquipQuote turns a small JSON file into a clean, printable quotation in
Markdown or HTML, and gets the arithmetic right every time.

## Features

- Line items with spec, unit, quantity and unit price
- Discount, freight and VAT (13% by default, configurable)
- Correct RMB amount-in-words, e.g. `叁万伍仟元整`, following invoice wording rules
- Markdown output for chat / docs, HTML output for printing or PDF
- Zero runtime dependencies — Python 3.10+ standard library only
- Usable as a CLI or as a Python library

## Quick start

```bash
pip install equipquote   # once published; for now: pip install -e .
equipquote demo
equipquote build examples/sample_quote.json --format md -o quote.md
equipquote build examples/sample_quote.json --format html -o quote.html
```

Input (`examples/sample_quote.json`):

```json
{
  "title": "激光打标机报价单",
  "seller": "某某智能装备有限公司",
  "buyer": "某某制造有限公司",
  "discount_rate": 0.05,
  "tax_rate": 0.13,
  "freight": 800,
  "items": [
    {"name": "光纤激光打标机", "spec": "30W", "unit": "台", "quantity": 1, "unit_price": 28000}
  ]
}
```

## Library usage

```python
from equipquote import Item, Quote, amount_to_chinese_upper

quote = Quote(seller="Acme Equipment", buyer="Beta Manufacturing",
              items=[Item(name="Fiber laser marker", spec="30W", unit_price=28000)])
print(quote.total)                         # tax-inclusive total
print(amount_to_chinese_upper(quote.total))
```

## Why this exists

The maintainer spent five years selling laser and industrial automation
equipment in China. The calculation and wording rules in this project come
from real quotation workflows, not from a tutorial. Roadmap: Excel export,
multi-page quotations, and customer follow-up reminders.

## 中文说明

EquipQuote 是给中小企业 B 端销售工程师用的设备报价单生成工具：输入一份
JSON，自动算小计、优惠、运费和增值税，并生成规范的人民币大写金额，
输出 Markdown 或可打印的 HTML 报价单。零第三方依赖。

## License

MIT
