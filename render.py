"""Render a Quote to Markdown or a printable HTML page."""
from __future__ import annotations

import html

from .chinese_upper import amount_to_chinese_upper
from .core import Quote

def _fmt(v) -> str:
    return f"{v:,.2f}"

def render_markdown(q: Quote) -> str:
    lines = [
        f"# {q.title}", "",
        f"- 报价方：{q.seller}",
        f"- 客户：{q.buyer}",
        f"- 联系人：{q.contact}",
        f"- 报价日期：{q.quote_date}（有效期至 {q.valid_until}）", "",
        "| # | 名称 | 规格 | 单位 | 数量 | 单价(元) | 金额(元) |",
        "|---|------|------|------|------|----------|----------|",
    ]
    for idx, item in enumerate(q.items, 1):
        lines.append(f"| {idx} | {item.name} | {item.spec} | {item.unit} | {item.quantity} | {_fmt(item.unit_price)} | {_fmt(item.line_total)} |")
    lines += [
        "",
        f"- 小计：{_fmt(q.subtotal)} 元",
        f"- 优惠：-{_fmt(q.discount_amount)} 元",
        f"- 运费：{_fmt(q.freight)} 元",
        f"- 税额（{q.tax_rate:.0%}）：{_fmt(q.tax_amount)} 元",
        f"- **含税总价：{_fmt(q.total)} 元**",
        f"- 大写：{amount_to_chinese_upper(q.total)}",
        "",
        "备注：本报价含税，税率按现行增值税率计算；交期与付款方式以正式合同为准。",
    ]
    return "\n".join(lines) + "\n"

def render_html(q: Quote) -> str:
    rows = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in
        [idx, i.name, i.spec, i.unit, i.quantity, _fmt(i.unit_price), _fmt(i.line_total)]) + "</tr>"
        for idx, i in enumerate(q.items, 1)
    )
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{html.escape(q.title)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:820px;margin:40px auto}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ccc;padding:8px}}</style>
</head><body><h1>{html.escape(q.title)}</h1>
<p>报价方：{html.escape(q.seller)}<br>客户：{html.escape(q.buyer)}<br>日期：{q.quote_date}，有效期至 {q.valid_until}</p>
<table><tr><th>#</th><th>名称</th><th>规格</th><th>单位</th><th>数量</th><th>单价(元)</th><th>金额(元)</th></tr>{rows}</table>
<p>小计：{_fmt(q.subtotal)} 元<br>优惠：-{_fmt(q.discount_amount)} 元<br>运费：{_fmt(q.freight)} 元<br>
税额：{_fmt(q.tax_amount)} 元<br><strong>含税总价：{_fmt(q.total)} 元</strong><br>大写：{amount_to_chinese_upper(q.total)}</p>
</body></html>
"""
