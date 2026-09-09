from __future__ import annotations

import argparse
from pathlib import Path

from .parser import extract_receipt_pdf
from .workbook import write_workbook


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract EFD receipt fields from PDF files")
    parser.add_argument("input_dir", type=Path, help="directory containing PDF receipts")
    parser.add_argument("-o", "--output", type=Path, default=Path("output/receipts.xlsx"))
    args = parser.parse_args()

    paths = sorted(args.input_dir.glob("*.pdf"))
    if not paths:
        parser.error(f"no PDF files found in {args.input_dir}")
    rows = [extract_receipt_pdf(path) for path in paths]
    write_workbook(rows, args.output)
    complete = sum(row.status == "OK" for row in rows)
    print(f"processed={len(rows)} complete={complete} output={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
