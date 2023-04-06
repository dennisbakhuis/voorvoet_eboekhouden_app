"""Verwerk de Zettle export naar een lijst van mutaties."""
import eboekhouden_python as ebh
import pandas as pd


def zettle_dataframe_to_mutatie(
    mutaties_raw: pd.DataFrame,
    zettle_rekening: str = "1020",
    zettle_kosten: str = "4560",
    zettle_kruispost: str = "2010",
    zettle_tijdelijk: str = "8140",
    bank_rekening: str = "1010",
):
    """Verwerk de Zettle export naar een lijst van mutaties."""
    mutaties = []
    for _, row in mutaties_raw.iterrows():
        if row["Type"] == "Kaartbetaling":
            # Kaartbetaling:
            # --------------
            # Het moet een factuurbetaling zijn maar we kunnen deze regels niet gemakklijk aan een factuur koppelen.
            # In plaats daarvan gaan we een mutatie aanmaken op een tijdelijke rekening die je later handmatig nog
            # moet wijzigen naar een factuurbetaling en koppelen aan een factuur.
            #
            # 1x Mutatie:
            # - geld ontvangen
            # - rekening 1020 (zettle rekening)
            # - tegenrekening 8140 (zettle tijdelijk)
            omschrijving = f"Zettle pintransactie {int(row['Bon'])} / betaald op {row['Datum betaling'].strftime('%Y-%m-%d %H:%M')}"
            mutatie = ebh.models.Mutatie.geld_ontvangen(
                datum=row["Datum betaling"].strftime("%Y-%m-%d"),
                rekening=zettle_rekening,
                omschrijving=omschrijving,
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=row["Bedrag"],
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_tijdelijk,
                    ),
                ],
            )
            mutaties.append(mutatie)
        elif row["Type"] == "Toeslag":
            # Toeslag:
            # --------
            # 1x Mutatie\
            # - geld uitgegeven
            # - rekening 1020 (zettle rekening)
            # - tegenrekening 4560 (zettle kosten)
            omschrijving = f"Kosten Zettle van pinbon {int(row['Bon'])} / betaald op {row['Datum betaling'].strftime('%Y-%m-%d %H:%M')}"
            mutatie = ebh.models.Mutatie.geld_uitgegeven(
                datum=row["Datum betaling"].strftime("%Y-%m-%d"),
                rekening=zettle_rekening,
                omschrijving=omschrijving,
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=abs(row["Bedrag"]),
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_kosten,
                    ),
                ],
            )
            mutaties.append(mutatie)
        elif row["Type"] == "Storting op bankrekening":
            # Storting op rekening:
            # ---------------------
            # 2x Mutatie\
            # Mutatie 1:
            # - geld uitgegeven
            # - rekening 1020 (zettle rekening)
            # - tegenrekening 2010 (kruispost zettle)

            # Mutatie 2:
            # - geld ontvangen
            # - rekening 1010 (bank)
            # - tegenrekening 2010 (kruispost zettle)
            omschrijving = f"Uitbetaling Zettle tot {row['Datum afhandeling']} / Saldo na overboeking: {row['Saldo']}"
            datum = row["Datum afhandeling"].strftime("%Y-%m-%d")
            mutatie = ebh.models.Mutatie.geld_uitgegeven(
                datum=datum,
                rekening=zettle_rekening,
                omschrijving=f"{omschrijving} (1/2)",
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=abs(row["Bedrag"]),
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_kruispost,
                    ),
                ],
            )
            mutaties.append(mutatie)
            mutatie = ebh.models.Mutatie.geld_ontvangen(
                datum=datum,
                rekening=bank_rekening,
                omschrijving=f"{omschrijving} (2/2)",
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=abs(row["Bedrag"]),
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_kruispost,
                    ),
                ],
            )
            mutaties.append(mutatie)
        elif row["Type"] == "Terugbetaling, kaartbetaling":
            # Terugbetaling:
            # --------------
            # Dit moet een correctie zijn op een factuur dus eigenlijk een factuurbetaling. Omdat de
            # factuur niet gekoppeld kan worden aan de regel in de Zettle export gaan we een mutatie
            # aanmaken op een tijdelijke rekening die je later handmatig nog moet wijzigen naar een
            # factuurbetaling en koppelen aan een factuur.
            #
            # 1x mutatie:
            # - geld uitgegeven
            # - rekening 1020 (debiteuren)
            # - tegenrekening 8140 (zettle tijdelijk)
            omschrijving = f"Terugbetaling Zettle pintransactie {int(row['Bon'])} / terugbetaald op {row['Datum betaling'].strftime('%Y-%m-%d %H:%M')}"
            mutatie = ebh.models.Mutatie.geld_uitgegeven(
                datum=row["Datum betaling"].strftime("%Y-%m-%d"),
                rekening=zettle_rekening,
                omschrijving=omschrijving,
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=abs(row["Bedrag"]),
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_tijdelijk,
                    ),
                ],
            )
            mutaties.append(mutatie)
        elif row["Type"] == "Toeslag, Terugbetaling":
            # Terugbetaling Toeslag:
            # ----------------------
            # 1x Mutatie\
            # - geld ontvangen
            # - rekening 1020 (zettle rekening)
            # - tegenrekening 4560 (zettle kosten)
            omschrijving = f"Terugbetaling Zettle kosten van pinbon {int(row['Bon'])} / betaald op {row['Datum betaling'].strftime('%Y-%m-%d %H:%M')}"
            mutatie = ebh.models.Mutatie.geld_ontvangen(
                datum=row["Datum betaling"].strftime("%Y-%m-%d"),
                rekening=zettle_rekening,
                omschrijving=omschrijving,
                mutatie_regels=[
                    ebh.models.MutatieRegel.from_bedrag(
                        bedrag_invoer=abs(row["Bedrag"]),
                        btw_code=ebh.constants.BtwCode.geen,
                        tegenrekening_code=zettle_kosten,
                    ),
                ],
            )
            mutaties.append(mutatie)

        else:
            raise ValueError(f"Unknown type in Zettle import: {row['Type']}")

    return mutaties
