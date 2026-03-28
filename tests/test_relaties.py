import io

from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
from streamlit.proto.Common_pb2 import FileURLs
import pandas as pd
import pytest
import eboekhouden_python as ebh

from .mock_client import MockClient
from voorvoet_app.pages.relaties import (
    process_relaties,
    select_new_relaties,
    generate_relatie_objects,
)


def create_relaties_excel(rows):
    """Create a minimal James EPD-style relaties Excel file in memory."""
    buf = io.BytesIO()
    header_rows = pd.DataFrame([
        ["Debiteuren"] + [""] * 13,
        ["Praktijk:", "Test Praktijk"] + [""] * 12,
        ["Datum:", "01-01-2025"] + [""] * 12,
        [""] * 14,
    ])
    data = pd.DataFrame(rows)
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        header_rows.to_excel(writer, index=False, header=False, startrow=0)
        data.to_excel(writer, index=False, startrow=4)
    buf.seek(0)
    return buf


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
                "Accountnaam": "test",
                "Geslacht": "Vrouw",
                "Initialen": "t.",
                "Tussenvoegsels": None,
                "Volledige naam": "t. test",
                "Betalingscondities": "Binnen 14 dagen",
                "Grootboekrekeningnummer debiteuren": 1300,
                "Straat": "kerkstraat",
                "Huisnummer inclusief toevoeging": "1",
                "Postcode": "1234AB",
                "Woonplaats": "Duckstad",
                "Land": "NL",
                "E-mail": "no@way.hosee",
            }
        ]
    )


def test_relaties_process_relaties(monkeypatch):
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

    result = process_relaties(uploaded_file)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 7)
    assert result.columns.tolist() == [
        "relatie_code",
        "Bedrijf/Naam",
        "Vestigingsadres",
        "Vestigingsadres postcode",
        "Vestigingsadres plaats",
        "Vestigingsadres land",
        "Bedrijf/Particulier",
    ]


def test_relaties_select_new_relaties(monkeypatch):
    monkeypatch.setattr("eboekhouden_python.EboekhoudenClient", MockClient)
    df = pd.DataFrame(
        [
            {"relatie_code": "1", "Bedrijf/Naam": "test", "Bedrijf/Particulier": "B"},
            {"relatie_code": "3", "Bedrijf/Naam": "test2", "Bedrijf/Particulier": "P"},
        ]
    )
    result = select_new_relaties(df)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 3)


def test_relaties_generate_relatie_objects():
    df = pd.DataFrame(
        [
            {
                "relatie_code": "1",
                "Bedrijf/Naam": "test",
                "Bedrijf/Particulier": "B",
                "Vestigingsadres": "kerkstraat",
                "Vestigingsadres postcode": "1234AB",
                "Vestigingsadres plaats": "Duckstad",
                "Vestigingsadres land": "NL",
            }
        ]
    )
    result = generate_relatie_objects(df)

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], ebh.models.Relatie)


RELATIE_ROW = {
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


def test_process_relaties_with_real_excel():
    excel_file = create_relaties_excel([RELATIE_ROW])
    result = process_relaties(excel_file)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 7)
    assert result["relatie_code"].iloc[0] == "JR-1"


def test_process_relaties_wrong_file_type():
    facturen_row = {
        "Debiteurennummer": 999,
        "Factuurnummer": 1,
        "Declaratienummer": float("nan"),
        "Naam": "Test",
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
    excel_file = create_facturen_excel([facturen_row])

    with pytest.raises(ValueError, match="Dit is geen geldig James EPD relaties bestand"):
        process_relaties(excel_file)
