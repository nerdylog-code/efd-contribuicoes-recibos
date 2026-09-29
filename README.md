> **Consolidated:** the document-conference flow this experiment belongs to now lives in [fiscal-document-automation](https://github.com/nerdylog-code/fiscal-document-automation) — document reading (PDF/XML), fiscal rules, reconciliation against the client spreadsheet and the review workbook. This repository is kept as history.

# EFD Contribuicoes Receipts

A local-first Python tool that extracts structured fields from text-layer EFD Contribuicoes receipt PDFs and writes a review-friendly Excel workbook. It demonstrates document parsing, explicit incomplete-status handling, and deterministic export without sending data to an external service.

This is a sanitized portfolio repository. The included fixture is synthetic; no real receipt, taxpayer identifier, workbook template, customer file, OCR output, or employer system is included.

## Features

- Parse receipt number, CNPJ, receipt date/time, receiving agent, and assessment period.
- Mark records `OK` only when all required fields are present; otherwise use `INCOMPLETE`.
- Batch-process PDFs from a local directory.
- Export normalized rows to `output/receipts.xlsx`.
- Run a deterministic demo without credentials or external APIs.

## Quickstart

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python demo.py
```

The demo reads `fixtures/synthetic_receipt.txt` and creates `output/demo_receipts.xlsx`.

For real text-layer PDFs:

```bash
python -m efd_receipts.cli ./path/to/pdf-directory --output output/receipts.xlsx
```

## Development

```bash
python -m pip install -e ".[test]"
python -m pytest
```

## Scope and limitations

- PDF extraction uses `pdfplumber` and expects a text layer. Scanned PDFs need a separately installed OCR pipeline and are not silently processed here.
- This project extracts fields for review; it does not validate a filing with government systems, calculate tax, or submit documents.
- Identifiers are emitted in the workbook because the tool models a local review workflow. Keep inputs and outputs outside version control and follow applicable privacy rules.
- No production, scale, savings, deployment, or coverage claims are made.

## License

MIT. See `LICENSE`.
