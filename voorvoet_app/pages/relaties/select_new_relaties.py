"""Select new relaties from relaties_raw."""
import eboekhouden_python as ebh
import pandas as pd


def select_new_relaties(
    relaties_raw: pd.DataFrame,
):
    """Select new relaties from relaties_raw."""
    client = ebh.EboekhoudenClient()
    existing_relaties = client.get_relaties()
    existing_relatie_codes = [x["Code"] for x in existing_relaties]

    new_relaties = relaties_raw.loc[~relaties_raw["relatie_code"].isin(existing_relatie_codes)]

    return new_relaties
