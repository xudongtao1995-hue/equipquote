"""Command-line interface: equipquote build quote.json --format md|html -o out.md"""
from __future__ import annotations

import argparse, json, pathlib, sys

from .core import Quote
from .render import render_html, render_markdown

_SAMPLE = {
    "title": "激光打标机报价单", "seller": "某某智能装备有限公司", "buyer": "某某制造有限公司",
    "contact": "张工", "discount_rate": 0.05, "tax_rate": 0.13, "freight": 800,
    "items": [
        {"name": "光纤激光打标机", "spec": "30W", "unit": "台", "quantity": 1, "unit_price": 28000},
        {"name": "旋转夹具", "spec": "D80", "unit": "套", "quantity": 1, "unit_price": 1500},
    ],
}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="equipquote", description="Industrial equipment quotation generator")
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="build a quotation from a JSON file")
    b.add_argument("input")
    b.add_argument("--format", choices=["md", "html"], default="md")
    b.add_argument("-o", "--output", default="")
    d = sub.add_parser("demo", help="print a sample quotation")
    d.add_argument("--format", choices=["md", "html"], default="md")
    args = parser.parse_args(argv)

    if args.cmd == "demo":
        quote = Quote.from_dict(json.loads(json.dumps(_SAMPLE)))
        text = render_html(quote) if args.format == "html" else render_markdown(quote)
        print(text)
        return 0

    data = json.loads(pathlib.Path(args.input).read_text(encoding="utf-8"))
    quote = Quote.from_dict(data)
    text = render_html(quote) if args.format == "html" else render_markdown(quote)
    if args.output:
        pathlib.Path(args.output).write_text(text, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main())
