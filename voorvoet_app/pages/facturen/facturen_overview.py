"""Facturen overview helper function."""
from typing import List
from eboekhouden_python.models import Mutatie
import pandas as pd


def facturen_overview(
    facturen: List[Mutatie],
) -> pd.DataFrame:
    """Return a DataFrame with the facturen overview."""
    rows = []
    for factuur in facturen:
        rows.append(
            {
                "Factuur": factuur.factuur_nummer,
                "Datum": factuur.datum,
                "Relatie": factuur.relatie_code,
                "Omschrijving": factuur.omschrijving.strip().replace("\n", " / "),
            }
        )

    return pd.DataFrame(rows)
