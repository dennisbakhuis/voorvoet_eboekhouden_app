"""Generate relatie objects."""
from typing import List

import eboekhouden_python as ebh
import pandas as pd


def generate_relatie_objects(to_be_added: pd.DataFrame) -> List[ebh.models.Relatie]:
    """Generate relatie objects."""
    relaties = []
    for _, row in to_be_added.iterrows():
        relatie = ebh.models.Relatie(
            relatie_code=row.relatie_code,
            bedrijf=row["Bedrijf/Naam"],
            bedrijf_particulier=row["Bedrijf/Particulier"],
            adres=row["Vestigingsadres"],
            postcode=row["Vestigingsadres postcode"],
            plaats=row["Vestigingsadres plaats"],
            land=row["Vestigingsadres land"],
        )
        relaties.append(relatie)

    return relaties
