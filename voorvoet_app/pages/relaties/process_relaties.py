"""Process relaties excel file to dataframe."""
from typing import BinaryIO, Union
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


def process_relaties(
    uploaded_file: Union[UploadedFile, BinaryIO],
    prefix_relatie: str = "JR-",
) -> pd.DataFrame:
    """Process relaties excel file to dataframe."""
    relaties_raw = pd.read_excel(uploaded_file, header=4, usecols=lambda x: isinstance(x, str) and "Unnamed" not in x)

    verwachte_kolommen = {
        "Debiteurennummer", "Accountnaam", "Geslacht", "Volledige naam",
        "Straat", "Huisnummer inclusief toevoeging", "Postcode", "Woonplaats", "Land",
    }
    ontbrekend = verwachte_kolommen - set(relaties_raw.columns)
    if ontbrekend:
        raise ValueError(
            f"Dit is geen geldig James EPD relaties bestand. "
            f"De volgende kolommen ontbreken: {', '.join(sorted(ontbrekend))}. "
            f"Controleer of je het juiste bestand hebt geüpload op de juiste pagina."
        )

    relaties_raw = relaties_raw.loc[relaties_raw["Debiteurennummer"] > 0]
    relaties_raw = (
        relaties_raw.assign(
            Naam=relaties_raw.apply(
                lambda x: f"{x['Volledige naam'].strip()} ({x['Geslacht'][0]})"
                if isinstance(x["Volledige naam"], str)
                else x["Accountnaam"],
                axis=1,
            ),
            Soort=relaties_raw.apply(
                lambda x: "P" if isinstance(x["Volledige naam"], str) else "B",
                axis=1,
            ),
            Vestigingsadres=relaties_raw.apply(
                lambda x: f"{x['Straat'].strip()} {x['Huisnummer inclusief toevoeging']}"
                if isinstance(x["Volledige naam"], str)
                else None,  # type: ignore
                axis=1,
            ),
            relatie_code=relaties_raw.apply(
                lambda x: f"{prefix_relatie}{x['Debiteurennummer']}",
                axis=1,
            ),
        )
        .rename(
            columns={
                "Naam": "Bedrijf/Naam",
                "Debiteurennummer": "Code",
                "Postcode": "Vestigingsadres postcode",
                "Woonplaats": "Vestigingsadres plaats",
                "Land": "Vestigingsadres land",
                "Soort": "Bedrijf/Particulier",
            }
        )
        .sort_values(by="Code")
        .loc[
            :,
            [
                "relatie_code",
                "Bedrijf/Naam",
                "Vestigingsadres",
                "Vestigingsadres postcode",
                "Vestigingsadres plaats",
                "Vestigingsadres land",
                "Bedrijf/Particulier",
            ],
        ]
    )
    relaties_raw = relaties_raw.where(pd.notnull(relaties_raw), None)  # type: ignore[arg-type]
    return relaties_raw
