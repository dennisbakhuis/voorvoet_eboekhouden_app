"""Mock EboekhoudenClient."""
import eboekhouden_python as ebh


class MockClient:
    """Mock EboekhoudenClient."""

    def __init__(self):
        """Init."""
        pass

    def get_relaties(self):
        """Mock get_relaties."""
        return [
            ebh.models.Relatie(
                relatie_code="1",
                bedrijf="test",
                bedrijf_particulier="B",
            ),
            ebh.models.Relatie(
                relatie_code="2",
                bedrijf="test2",
                bedrijf_particulier="P",
            ),
        ]

    def get_mutaties(self, factuur_nummer):
        """Mock get_mutaties."""
        if factuur_nummer == "1":
            return ["yes"]
        return []

    def mutatie_exists(self, mutatie):
        """Mock mutatie_exists."""
        if mutatie.omschrijving == "test1":
            return True
        return False
