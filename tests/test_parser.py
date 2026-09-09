from efd_receipts.parser import parse_receipt_text


VALID_TEXT = """Contribuinte: EXEMPLO SINTETICO LTDA
CNPJ: 00.000.000/0000-00
Período de apuração: 01/01/2026 a 31/01/2026
recebida via Internet pelo Agente Receptor SERPRO em 15/02/2026 às 10:20:30
Número do Recibo: AA.AA.AA.AA.AA.AA.AA.AA.AA.AA.BB-C
"""


def test_parse_complete_synthetic_receipt() -> None:
    result = parse_receipt_text(VALID_TEXT, "sample.txt")
    assert result.status == "OK"
    assert result.source_file == "sample.txt"
    assert result.cnpj == "00.000.000/0000-00"
    assert result.receiving_agent == "SERPRO"
    assert result.period.startswith("01/01/2026")


def test_parse_missing_fields_is_explicitly_incomplete() -> None:
    result = parse_receipt_text("CNPJ: 00.000.000/0000-00", "partial.txt")
    assert result.status == "INCOMPLETE"
    assert result.receipt_number == ""
    assert result.period == ""
