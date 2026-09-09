from pathlib import Path

from efd_receipts.parser import parse_receipt_text
from efd_receipts.workbook import write_workbook


ROOT = Path(__file__).parent
fixture = ROOT / "fixtures" / "synthetic_receipt.txt"
output = ROOT / "output" / "demo_receipts.xlsx"
row = parse_receipt_text(fixture.read_text(encoding="utf-8"), fixture.name)
write_workbook([row], output)
print(f"status={row.status} output={output}")
