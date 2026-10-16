"""Retail checkout, safe discount previews, and receipt logging."""

from dataclasses import dataclass, field
import math
import re
import secrets

PRICE_LIST = {"pen": 10, "notebook": 45, "bag": 799, "bottle": 150}


@dataclass
class SalesState:
    """Own the running sales total, pending receipts, and stock adjustments."""

    total: float = 0.0
    receipt_lines: list[str] = field(default_factory=list)
    stock: dict[str, int] = field(default_factory=dict)


STATE = SalesState()


def process_checkout(cart_items, tax_rate=0.05, receipts=None):
    """Validate the whole cart before recording a taxed checkout."""
    if receipts is None:
        receipts = []
    if (isinstance(tax_rate, bool)
            or not isinstance(tax_rate, (int, float))
            or not math.isfinite(tax_rate) or not 0 <= tax_rate <= 1):
        raise ValueError("Tax rate must be a number between 0 and 1")
    subtotal = 0
    for item, quantity in cart_items:
        if item not in PRICE_LIST:
            raise ValueError(f"Unknown product: {item}")
        if (isinstance(quantity, bool)
                or not isinstance(quantity, int) or quantity <= 0):
            raise ValueError("Quantity must be a positive integer")
        subtotal += PRICE_LIST[item] * quantity
    total = round(subtotal * (1 + tax_rate), 2)
    receipts.append(total)
    STATE.total = round(STATE.total + total, 2)
    receipt_id = secrets.randbelow(9000) + 1000
    STATE.receipt_lines.append(f"Receipt #{receipt_id} total={total:.2f}")
    return total


def apply_promo_code(code_str):
    """Preview a safe discount without changing recorded sales."""
    match = re.fullmatch(r"total\s*([*-])\s*(\d+(?:\.\d+)?)", code_str.strip())
    if match is None:
        raise ValueError("Use total * 0.9 or total - 50")
    operator, value = match.groups()
    amount = float(value)
    if operator == "*":
        if not 0 <= amount <= 1:
            raise ValueError("Discount multiplier must be between 0 and 1")
        return round(STATE.total * amount, 2)
    if amount > STATE.total:
        raise ValueError("Discount cannot exceed the sales total")
    return round(STATE.total - amount, 2)


def update_stock(item, qty):
    """Record stock additions separately from product prices."""
    if item not in PRICE_LIST:
        raise ValueError(f"Unknown product: {item}")
    if isinstance(qty, bool) or not isinstance(qty, int) or qty <= 0:
        raise ValueError("Stock addition must be a positive integer")
    STATE.stock[item] = STATE.stock.get(item, 0) + qty
    print("Stock updated for", item, "by", qty)


def save_receipt_log(file="pos_log.txt"):
    """Append pending receipts once, closing the UTF-8 log reliably."""
    with open(file, "a", encoding="utf-8") as log_file:
        for line in STATE.receipt_lines:
            log_file.write(line + "\n")
    STATE.receipt_lines.clear()


def print_sales():
    """Display the running sales total."""
    print(f"Sales so far: {STATE.total:.2f}")


def main():
    """Demonstrate checkouts and report invalid inputs."""
    carts = [
        ([("pen", 3), ("notebook", 2)], 0.05),
        ([("bag", 1), ("laptop", 1)], 0.05),
        ([("bottle", -4)], 0.05),
        ([("pen", "2")], -1),
    ]
    for number, (cart, tax_rate) in enumerate(carts, start=1):
        try:
            print(f"Bill {number}: {process_checkout(cart, tax_rate):.2f}")
        except ValueError as error:
            print(f"Bill {number} rejected: {error}")
    try:
        update_stock("laptop", 5)
    except ValueError as error:
        print(f"Stock update rejected: {error}")
    print(f"After promo: {apply_promo_code('total * 0.9'):.2f}")
    code = input("Enter promo code (e.g. total - 50): ") or "total - 50"
    try:
        print(f"After your promo: {apply_promo_code(code):.2f}")
    except ValueError as error:
        print(f"Promo rejected: {error}")
    save_receipt_log()
    print_sales()


if __name__ == "__main__":
    main()
