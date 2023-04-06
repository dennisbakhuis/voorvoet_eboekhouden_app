from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
import pandas as pd
import eboekhouden_python as ebh

from .mock_client import MockClient
from voorvoet_app.pages.relaties import (
    process_relaties,
    select_new_relaties,
    generate_relatie_objects,
)


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
            id=0,
            name="relaties.xlsx",
            type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data=b"hellow",
        )
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
