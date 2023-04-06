from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec
import pandas as pd
import pytest
import eboekhouden_python as ebh

from .mock_client import MockClient
from voorvoet_app.pages.zettle import (
    zettle_import_from_excel,
    zettle_dataframe_to_mutatie,
    zettle_select_new_transactions,
    zettle_mutatie_overview,
)


def mock_read_excel(*args, **kwargs):
    return pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "Kaartbetaling",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )


def test_zettle_zettle_import_from_excel(monkeypatch):
    monkeypatch.setattr("pandas.read_excel", mock_read_excel)
    uploaded_file = UploadedFile(
        record=UploadedFileRec(
            id=0,
            name="relaties.xlsx",
            type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            data=b"hellow",
        )
    )

    result = zettle_import_from_excel(uploaded_file)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 6)
    assert result.columns.tolist() == [
        "Datum afhandeling",
        "Datum betaling",
        "Bon",
        "Type",
        "Bedrag",
        "Saldo",
    ]


def test_zettle_zettle_dataframe_to_mutatie():
    # kaartbetaling
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "Kaartbetaling",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    result = zettle_dataframe_to_mutatie(df)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2023-03-01"
    assert len(result) == 1
    assert result[0].soort == ebh.constants.MutatieSoort.geld_ontvangen

    # toeslag
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "Toeslag",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    result = zettle_dataframe_to_mutatie(df)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2023-03-01"
    assert len(result) == 1
    assert result[0].soort == ebh.constants.MutatieSoort.geld_uitgegeven

    # toeslag
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": None,
                "Bon": 1.0,
                "Type": "Storting op bankrekening",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    result = zettle_dataframe_to_mutatie(df)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2023-03-02"
    assert len(result) == 2
    assert result[0].soort == ebh.constants.MutatieSoort.geld_uitgegeven
    assert result[1].soort == ebh.constants.MutatieSoort.geld_ontvangen

    # terugbetaling
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "Terugbetaling, kaartbetaling",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    result = zettle_dataframe_to_mutatie(df)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2023-03-01"
    assert len(result) == 1
    assert result[0].soort == ebh.constants.MutatieSoort.geld_uitgegeven

    # toeslag
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "Toeslag, Terugbetaling",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    result = zettle_dataframe_to_mutatie(df)

    assert isinstance(result, list)
    assert isinstance(result[0], ebh.models.Mutatie)
    assert result[0].datum == "2023-03-01"
    assert len(result) == 1
    assert result[0].soort == ebh.constants.MutatieSoort.geld_ontvangen

    # error
    df = pd.DataFrame(
        [
            {
                "Datum afhandeling": pd.Timestamp("2023-03-02 00:58:04.964000"),
                "Datum betaling": pd.Timestamp("2023-03-01 08:13:24.864000"),
                "Bon": 1.0,
                "Type": "yup",
                "Bedrag": 100,
                "Saldo": 100,
            },
        ]
    )

    with pytest.raises(ValueError):
        result = zettle_dataframe_to_mutatie(df)


def test_zettle_zettle_mutatie_overview():
    """Test the zettle_mutatie_overview function."""
    fake_data = [
        ebh.models.Mutatie.geld_ontvangen(
            datum="2023-03-01",
            rekening="1234",
            omschrijving="test",
            mutatie_regels=[
                ebh.models.MutatieRegel.from_bedrag(
                    bedrag_invoer=100,
                    btw_code=ebh.constants.BtwCode.hoog_verkoop_21,
                    tegenrekening_code="1234",
                )
            ],
        )
    ]
    result = zettle_mutatie_overview(fake_data)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (1, 6)
    assert result.columns.tolist() == [
        "Datum",
        "Soort",
        "Bedrag",
        "Omschrijving",
        "Rekening",
        "Tegenrekening",
    ]


def test_zettle_zettle_select_new_transactions(monkeypatch):
    """Test the zettle_select_new_transactions function."""
    monkeypatch.setattr("eboekhouden_python.EboekhoudenClient", MockClient)

    class DummyMutation:
        def __init__(self, omschrijving):
            self.omschrijving = omschrijving

    fake_data = [
        DummyMutation("test1"),
        DummyMutation("test2"),
    ]

    to_be_added, existing = zettle_select_new_transactions(fake_data)  # type: ignore

    assert isinstance(to_be_added, list)
    assert len(to_be_added) == 1
    assert isinstance(existing, list)
    assert len(existing) == 1
