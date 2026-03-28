"""Import Zettle mutaties from Excel file into DataFrame."""
from typing import Union
from pathlib import Path

import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


def zettle_import_from_excel(uploaded_file: Union[UploadedFile, str, Path]) -> pd.DataFrame:
    """Import Zettle mutaties from Excel file into DataFrame."""
    mutaties_raw = pd.read_excel(uploaded_file, skiprows=0)

    verwachte_kolommen = {"Datum afhandeling", "Datum betaling", "Bon", "Type", "Bedrag", "Saldo"}
    ontbrekend = verwachte_kolommen - set(mutaties_raw.columns)
    if ontbrekend:
        raise ValueError(
            f"Dit is geen geldig Zettle export bestand. "
            f"De volgende kolommen ontbreken: {', '.join(sorted(ontbrekend))}. "
            f"Controleer of je het juiste bestand hebt geüpload op de juiste pagina."
        )

    mutaties_raw = mutaties_raw.sort_values(by=["Datum afhandeling", "Datum betaling"]).reset_index(
        drop=True
    )
    mutaties_raw = mutaties_raw.where(pd.notnull(mutaties_raw), None)  # type: ignore[arg-type]

    return mutaties_raw
