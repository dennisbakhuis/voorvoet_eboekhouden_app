"""Facturen overview helper function."""

import pandas as pd
from eboekhouden_python.models import Mutatie


def facturen_overview(
    facturen: list[Mutatie],
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
