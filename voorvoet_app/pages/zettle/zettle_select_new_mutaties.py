"""Select new Zettle transactions from DataFrame."""

import eboekhouden_python as ebh


def zettle_select_new_mutaties(
    zettle_raw: list[ebh.models.Mutatie],
) -> tuple[list[ebh.models.Mutatie], list[ebh.models.Mutatie]]:
    """Select new Zettle transactions from DataFrame."""
    client = ebh.EboekhoudenClient()

    to_be_added, already_exists = [], []
    for mutatie in zettle_raw:
        if not client.mutatie_exists(mutatie):
            to_be_added.append(mutatie)
        else:
            already_exists.append(mutatie)

    return to_be_added, already_exists
