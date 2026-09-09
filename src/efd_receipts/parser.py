from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


RECEIPT_NUMBER_RE = re.compile(r"(?:[0-9A-F]{2}\.){10,}[0-9A-F]{2}-[0-9A-F]")
CNPJ_RE = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
PERIOD_RE = re.compile(
    r"Período de apuração:\s*"
    r"([0-9]{2}/[0-9]{2}/[0-9]{4}\s+a\s+[0-9]{2}/[0-9]{2}/[0-9]{4})",
    re.IGNORECASE,
)
DATE_TIME_RE = re.compile(
    r"\bem\s+([0-9]{2}/[0-9]{2}/[0-9]{4})\s+às\s+([0-9]{2}:[0-9]{2}:[0-9]{2})",
    re.IGNORECASE,
)
AGENT_RE = re.compile(r"Agente Receptor\s+([A-Z0-9]+)", re.IGNORECASE)


@dataclass(frozen=True)
class ReceiptData:
    source_file: str
    cnpj: str
    receipt_number: str
    received_date: str
    received_time: str
    receiving_agent: str
    period: str
    status: str


def parse_receipt_text(text: str, source_file: str = "") -> ReceiptData:
    """Parse text extracted from an EFD receipt without retaining raw text."""
    compact = re.sub(r"\s+", "", text)
    receipt = RECEIPT_NUMBER_RE.search(compact)
    cnpj = CNPJ_RE.search(text)
    period = PERIOD_RE.search(text)
    date_time = DATE_TIME_RE.search(text)
    agent = AGENT_RE.search(text)

    values = {
        "cnpj": cnpj.group(0) if cnpj else "",
        "receipt_number": receipt.group(0) if receipt else "",
        "received_date": date_time.group(1) if date_time else "",
        "received_time": date_time.group(2) if date_time else "",
        "receiving_agent": agent.group(1).upper() if agent else "SERPRO",
        "period": period.group(1) if period else "",
    }
    required = (values["cnpj"], values["receipt_number"], values["received_date"], values["received_time"], values["period"])
    return ReceiptData(
        source_file=source_file,
        **values,
        status="OK" if all(required) else "INCOMPLETE",
    )


def extract_receipt_pdf(path: Path) -> ReceiptData:
    """Extract and parse a text-layer PDF; OCR is intentionally out of scope."""
    import pdfplumber

    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    return parse_receipt_text(text, path.name)
