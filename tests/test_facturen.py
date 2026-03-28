import io
import math

import pandas as pd
import pytest
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
from streamlit.proto.Common_pb2 import FileURLs

import eboekhouden_python as ebh

from .mock_client import MockClient
from voorvoet_app.pages.facturen import (
    process_facturen,
    select_new_facturen,
    facturen_overview,
)


def create_facturen_excel(rows):
    """Create a minimal James EPD-style facturen Excel file in memory."""
    buf = io.BytesIO()
    header_rows = pd.DataFrame([
        ["Facturen en declaraties"] + [""] * 13,
        ["Praktijk:", "Test Praktijk"] + [""] * 12,
        ["Datum:", "01-01-2025"] + [""] * 12,
    ])
    data = pd.DataFrame(rows)
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        header_rows.to_excel(writer, index=False, header=False, startrow=0)
        data.to_excel(writer, index=False, startrow=3)
    buf.seek(0)
    return buf


def mock_read_excel(*args, **kwargs):
    return pd.DataFrame(
        [
            {
                "Debiteurennummer": 1,
                "Factuurnummer": 1,
                "Declaratienummer": math.nan,
                "Naam": "test",
                "Behandelaar": "t. test",
                "Locatie": "test",
                "Factuurdatum": "01-01-2020",
                "Consult datum": "01-02-2020",
                "Beschrijving": "geweldige behandeling",
                "Betalingsconditie": 14,
                "Grootboekrekening omzet": 8060,
                "Bedrag": 100,
                "BTW code": 0.21,
                "BTW bedrag": 21.0,
            },
            {
                "Debiteurennummer": 1,
                "Factuurnummer": 2,
                "Declaratienummer": 1,
                "Naam": "test",
                "Behandelaar": "t. test",
                "Locatie": "test",
                "Factuurdatum": "01-01-2020",
                "Consult datum": None,
                "Beschrijving": "geweldige behandeling",
                "Betalingsconditie": 14,
                "Grootboekrekening omzet": 8060,
                "Bedrag": 100,
                "BTW code": 0.21,
                "BTW bedrag": 21.0,
            },
        ]
    )


def test_facturen_process_facturen(monkeypatch):
    monkeypatch.setattr("pandas.read_excel", mock_read_excel)
    uploaded_file = UploadedFile(
        record=UploadedFileRec(
            file_id="test",
            name="relaties.xlsx",
            type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data=b"hellow",
        ),
        file_urls=FileURLs(),
    )

    result = process_facturen(uploaded_file)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2020-01-01"
    assert len(result) == 2


def test_facturen_select_new_facturen(monkeypatch):
    monkeypatch.setattr("eboekhouden_python.EboekhoudenClient", MockClient)

    class DummyMutatie:
        def __init__(self, factuur_nummer):
            self.factuur_nummer = factuur_nummer

    facturen_raw = [DummyMutatie("1"), DummyMutatie("2")]
    result = select_new_facturen(facturen_raw=facturen_raw)

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].factuur_nummer == "2"


def test_facturen_facturen_overview():
    class DummyMutatie:
        def __init__(self, factuur_nummer, datum, relatie_code, omschrijving):
            self.factuur_nummer = factuur_nummer
            self.datum = datum
            self.relatie_code = relatie_code
            self.omschrijving = omschrijving

    facturen_raw = [
        DummyMutatie("1", "2020-01-01", "1", "test"),
        DummyMutatie("2", "2020-01-01", "1", "test"),
    ]

    overview = facturen_overview(facturen=facturen_raw)  # type: ignore

    assert isinstance(overview, pd.DataFrame)
    assert overview.shape == (2, 4)


FACTUUR_ROW = {
    "Debiteurennummer": 999,
    "Factuurnummer": 1,
    "Declaratienummer": float("nan"),
    "Naam": "Test Patient",
    "Behandelaar": "T. Test",
    "Locatie": "Testlaan",
    "Factuurdatum": "01-01-2025",
    "Consult datum": "01-01-2025",
    "Beschrijving": "Test behandeling",
    "Betalingsconditie": "PIN",
    "Grootboekrekening omzet": 8060,
    "Bedrag": 46.5,
    "BTW code": 0.21,
    "BTW bedrag": 8.08,
}


def test_process_facturen_with_real_excel():
    excel_file = create_facturen_excel([FACTUUR_ROW])
    result = process_facturen(excel_file)

    assert len(result) == 1
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2025-01-01"
    assert result[0].relatie_code == "JR-999"
    assert result[0].factuur_nummer == "JF-1"


def test_process_facturen_with_zero_int_btw():
    row = {**FACTUUR_ROW, "BTW code": 0, "BTW bedrag": 0}
    excel_file = create_facturen_excel([row])
    result = process_facturen(excel_file)

    assert len(result) == 1


def test_process_facturen_with_unknown_btw():
    row = {**FACTUUR_ROW, "BTW code": 0.06}
    excel_file = create_facturen_excel([row])

    with pytest.raises(ValueError, match="Onbekende BTW code"):
        process_facturen(excel_file)


def test_process_facturen_wrong_file():
    relatie_row = {
        "Debiteurennummer": 1,
        "Accountnaam": "Test BV",
        "Geslacht": "Vrouw",
        "Initialen": "t.",
        "Tussenvoegsels": None,
        "Volledige naam": "t. test",
        "Betalingscondities": "Binnen 14 dagen",
        "Grootboekrekeningnummer debiteuren": 1300,
        "Straat": "Kerkstraat",
        "Huisnummer inclusief toevoeging": "1",
        "Postcode": "1234AB",
        "Woonplaats": "Duckstad",
        "Land": "NL",
        "E-mail": "test@example.com",
    }
    buf = io.BytesIO()
    header_rows = pd.DataFrame([
        ["Debiteuren"] + [""] * 13,
        ["Praktijk:", "Test"] + [""] * 12,
        ["Datum:", "01-01-2025"] + [""] * 12,
        [""] * 14,
    ])
    data = pd.DataFrame([relatie_row])
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        header_rows.to_excel(writer, index=False, header=False, startrow=0)
        data.to_excel(writer, index=False, startrow=4)
    buf.seek(0)

    with pytest.raises(ValueError, match="Dit is geen geldig James EPD facturen bestand"):
        process_facturen(buf)


def test_process_facturen_with_timestamp_dates():
    row = {
        **FACTUUR_ROW,
        "Factuurdatum": pd.Timestamp("2025-01-01"),
        "Consult datum": pd.Timestamp("2025-01-01"),
    }
    excel_file = create_facturen_excel([row])
    result = process_facturen(excel_file)

    assert result[0].datum == "2025-01-01"
