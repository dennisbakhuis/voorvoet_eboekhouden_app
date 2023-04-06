"""Overview of new Zettle transactions."""
from typing import List
import pandas as pd
import eboekhouden_python as ebh


def zettle_mutatie_overview(new_mutaties: List[ebh.models.Mutatie]) -> pd.DataFrame:
    """Overview of new Zettle transactions."""
    rows = []
    for ix, mutatie in enumerate(new_mutaties):
        bedrag = mutatie.mutatie_regels[0].bedrag_invoer
        tegenrekening = mutatie.mutatie_regels[0].tegenrekening_code
        rows.append(
            {
                "Volgnummer": ix + 1,
                "Datum": mutatie.datum,
                "Soort": mutatie.soort,
                "Bedrag": bedrag,
                "Omschrijving": mutatie.omschrijving,
                "Rekening": mutatie.rekening,
                "Tegenrekening": tegenrekening,
            }
        )
    return pd.DataFrame(rows).set_index("Volgnummer")
