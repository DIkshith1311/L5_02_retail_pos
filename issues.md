# Static analysis findings

Line numbers refer to the original starter file. Bandit severity is reported by the tool; other priorities are our assessment. No findings are suppressed.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B307 / W0123: eval (Medium) | Security | 27 | User input can execute Python code. | Parse only total * decimal or total - decimal; validate discount bounds. |
| W0102: mutable default (Medium priority) | Bug | 10 | Receipt list is shared across calls. | Use None and create a new list per call. |
| W0702 / E722: bare except (Medium priority) | Bug | 16 | Invalid products and quantities silently disappear from a bill. | Validate the entire cart and raise explicit ValueError before modifying totals. |
| B110 / W0718: swallowed exception (Low Bandit severity) | Bug | 33-34 | Stock errors are hidden. | Validate product and quantity; report invalid updates. |
| B311: random receipt identifier (Low) | Security/tool finding | 21 | Bandit flags random.randint; these IDs are labels, not security tokens. | Use secrets.randbelow to satisfy the lab; four-digit labels are still not guaranteed unique. |
| R1732 / W1514: file handling | Reliability | 37-39 | Receipt log is not explicitly closed and encoding is unspecified. | Use a with block and UTF-8; clear pending lines after successful writing. |
| W0603 / C0103: global sales state | Maintainability | 7, 11 | Global rebinding complicates state ownership. | Store totals, pending logs, and stock in a named state object. |
| C0114 / C0116: missing documentation | Maintainability | 1, 10, 24, 29, 36, 41, 44 | Module and functions lack descriptions. | Add docstrings. |
| C0103: printSales naming | Style | 41 | Function name is not snake_case. | Rename to print_sales. |
| W0611 / F401, F841 | Quality | 1, 3, 26 | Unused imports and eval-only variable. | Remove unused imports and replace eval. |
| E302 / E305 / E501 / C0209 | Style | 10, 21, 24, 29, 36, 41, 44, 56 | Missing blank lines, long line, and old string formatting. | Apply PEP 8 spacing, wrap long lines, and use f-strings. |

## Additional manual findings

- Negative and nonnumeric quantities and negative tax rates must be rejected.
- Unknown products must not silently produce partial bills.
- Stock updates previously assigned a price to itself; maintain separate stock adjustments without changing prices. Initial inventory is not provided, so stock is not enforced at checkout.
- Guard main() so importing the module does not prompt for input or write a receipt.
- Invalid demonstration inputs should print an error and let the remaining demonstration continue.
- Promo calculations preserve the starter's behaviour: they preview a discount on cumulative sales and do not change recorded sales.
