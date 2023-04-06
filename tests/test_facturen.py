import math

import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

import eboekhouden_python as ebh

from .mock_client import MockClient
from voorvoet_app.pages.facturen import (
    process_facturen,
    select_new_facturen,
    facturen_overview,
)


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
            id=0,
            name="relaties.xlsx",
            type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data=b"hellow",
        )
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
