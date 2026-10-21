"""Convert a monetary amount to Chinese uppercase RMB wording.

Example: Decimal("1234.56") -> "壹仟贰佰叁拾肆元伍角陆分"
This follows the wording conventions used on Chinese invoices and quotations.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

_DIGITS = "零壹贰叁肆伍陆柒捌玖"
_UNITS = ["", "拾", "佰", "仟"]
_BIG_UNITS = ["", "万", "亿", "兆"]

def _four_digits(num: int) -> str:
    """Render an integer 0..9999 without its big unit."""
    if num == 0:
        return ""
    chars: list[str] = []
    zero_pending = False
    for pos in range(3, -1, -1):
        digit = (num // (10 ** pos)) % 10
        if digit == 0:
            if chars:
                zero_pending = True
            continue
        if zero_pending:
            chars.append(_DIGITS[0])
            zero_pending = False
        chars.append(_DIGITS[digit] + _UNITS[pos])
    return "".join(chars)

def _integer_part(num: int) -> str:
    if num == 0:
        return _DIGITS[0]
    groups: list[str] = []
    idx = 0
    while num > 0:
        group = num % 10000
        rendered = _four_digits(group)
        if rendered:
            # A group below 1000 after a higher group needs a leading zero.
            if group < 1000 and num >= 10000:
                rendered = _DIGITS[0] + rendered
            groups.append(rendered + _BIG_UNITS[idx])
        elif groups:
            groups.append(_DIGITS[0])
        num //= 10000
        idx += 1
    text = "".join(reversed(groups))
    # Collapse any accidental double zeros.
    while "零零" in text:
        text = text.replace("零零", "零")
    return text.strip("零")

def amount_to_chinese_upper(amount) -> str:
    value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if value < 0:
        return "负" + amount_to_chinese_upper(-value)
    integer = int(value)
    cents = int((value - Decimal(integer)) * 100)
    jiao, fen = divmod(cents, 10)
    result = _integer_part(integer) + "元"
    if jiao == 0 and fen == 0:
        return result + "整"
    if jiao:
        result += _DIGITS[jiao] + "角"
    elif fen:
        result += "零"
    if fen:
        result += _DIGITS[fen] + "分"
    else:
        result += "整"
    return result
