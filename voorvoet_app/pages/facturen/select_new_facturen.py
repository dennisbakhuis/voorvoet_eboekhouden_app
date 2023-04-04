"""Select new facturen from raw facturen."""
import time
import eboekhouden_python as ebh


def select_new_facturen(facturen_raw):
    """Select new facturen from raw facturen."""
    client = ebh.EboekhoudenClient()
    to_be_added = []
    for factuur in facturen_raw:
        response = client.get_mutaties(
            factuur_nummer=factuur.factuur_nummer,
        )
        if not response:
            to_be_added.append(factuur)
        time.sleep(0.1)

    return to_be_added
