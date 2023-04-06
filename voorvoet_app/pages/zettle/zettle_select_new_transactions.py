"""Select new Zettle transactions from DataFrame."""
from typing import List, Tuple
import eboekhouden_python as ebh


def zettle_select_new_transactions(
    zettle_raw: List[ebh.models.Mutatie],
) -> Tuple[List[ebh.models.Mutatie], List[ebh.models.Mutatie]]:
    """Select new Zettle transactions from DataFrame."""
    client = ebh.EboekhoudenClient()

    to_be_added, already_exists = [], []
    for mutatie in zettle_raw:
        if not client.mutatie_exists(mutatie):
            to_be_added.append(mutatie)
        else:
            already_exists.append(mutatie)

    return to_be_added, already_exists
