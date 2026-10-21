"""Core quotation model and calculations."""
from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
import datetime as _dt

def _d(v) -> Decimal:
    return Decimal(str(v))

def _money(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

@dataclass
class Item:
    name: str
    spec: str = ""
    unit: str = "台"
    quantity: float = 1
    unit_price: float = 0

    @property
    def line_total(self) -> Decimal:
        return _money(_d(self.quantity) * _d(self.unit_price))

@dataclass
class Quote:
    title: str = "设备报价单"
    seller: str = ""
    buyer: str = ""
    contact: str = ""
    items: list[Item] = field(default_factory=list)
    discount_rate: float = 0       # 0.05 means 5% off
    tax_rate: float = 0.13         # China VAT 13% by default
    freight: float = 0
    validity_days: int = 15
    quote_date: str = ""

    def __post_init__(self):
        if not self.quote_date:
            self.quote_date = _dt.date.today().isoformat()
        if not (0 <= _d(self.discount_rate) < 1):
            raise ValueError("discount_rate must be in [0, 1)")
        if _d(self.tax_rate) < 0:
            raise ValueError("tax_rate must be >= 0")
        if not self.items:
            raise ValueError("a quote needs at least one item")

    @property
    def subtotal(self) -> Decimal:
        return _money(sum((i.line_total for i in self.items), Decimal("0")))

    @property
    def discount_amount(self) -> Decimal:
        return _money(self.subtotal * _d(self.discount_rate))

    @property
    def discounted(self) -> Decimal:
        return _money(self.subtotal - self.discount_amount)

    @property
    def tax_amount(self) -> Decimal:
        return _money((_d(self.discounted) + _d(self.freight)) * _d(self.tax_rate))

    @property
    def total(self) -> Decimal:
        return _money(self.discounted + _d(self.freight) + self.tax_amount)

    @property
    def valid_until(self) -> str:
        d = _dt.date.fromisoformat(self.quote_date)
        return (d + _dt.timedelta(days=self.validity_days)).isoformat()

    @classmethod
    def from_dict(cls, data: dict) -> "Quote":
        items = [Item(**i) for i in data.pop("items", [])]
        return cls(items=items, **data)
