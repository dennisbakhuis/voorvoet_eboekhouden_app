"""Process facturen from Excel file to e-Boekhouden format."""
import datetime
import math
import pandas as pd
import eboekhouden_python as ebh
from streamlit.runtime.uploaded_file_manager import UploadedFile


btw_codes = {
    0: ebh.constants.BtwCode.geen,
    0.0: ebh.constants.BtwCode.geen,
    0.21: ebh.constants.BtwCode.hoog_verkoop_21,
    0.09: ebh.constants.BtwCode.laag_verkoop_9,
}


def flip_date(date):
    """Flip date from DD-MM-YYYY to YYYY-MM-DD."""
    return datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")


def process_facturen(
    uploaded_file: UploadedFile,
    prefix_factuur: str = "JF-",
    prefix_relatie: str = "JR-",
    debiteur_rekening: str = "1300",
):
    """Process facturen from Excel file to e-Boekhouden format."""
    facturen_raw = pd.read_excel(uploaded_file, header=3)
    facturen_raw.loc[:, "Declaratienummer"] = facturen_raw.Declaratienummer.apply(
        lambda x: str(int(x)) if not math.isnan(x) else None,  # type: ignore
    )
    facturen_raw = facturen_raw.where(pd.notnull(facturen_raw), None)

    facturen = []
    for factuur_nummer_original, factuurregels_raw in facturen_raw.groupby("Factuurnummer"):
        factuur_nummer = f"{prefix_factuur}{factuur_nummer_original}"
        factuurregels, relatie, declaratienummer = [], [], []
        factuurdatum, consultdatum = [], []
        omschrijvingen, betalingsconditie, naam = [], [], []

        for _, regel in factuurregels_raw.iterrows():
            factuurregels.append(
                ebh.models.MutatieRegel.from_bedrag(
                    bedrag_invoer=regel.Bedrag,
                    btw_code=btw_codes[regel["BTW code"]],
                    tegenrekening_code=regel["Grootboekrekening omzet"],
                )
            )

            relatie.append(regel.Debiteurennummer)
            if regel.Declaratienummer:
                declaratienummer.append(regel.Declaratienummer)

            factuurdatum.append(regel.Factuurdatum)

            if regel["Consult datum"]:
                consultdatum.append(regel["Consult datum"])

            if regel["Beschrijving"]:
                omschrijvingen.append(regel["Beschrijving"])

            if regel["Betalingsconditie"]:
                betalingsconditie.append(regel["Betalingsconditie"])

            if regel["Naam"]:
                naam.append(regel["Naam"])

        if len(set(relatie)) > 1:  # pragma: no cover
            raise ValueError("Meerdere relaties, dat zou niet mogen...")
        relatie = f"{prefix_relatie}{relatie[0]}"

        print(f" ---> declaratienummer: {declaratienummer}")

        if declaratienummer:
            if len(set(declaratienummer)) > 1:  # pragma: no cover
                raise ValueError("Meerdere declaratienummers, dat zou niet mogen...")
            declaratienummer = str(int(declaratienummer[0]))
        else:
            declaratienummer = None

        if len(set(factuurdatum)) > 1:  # pragma: no cover
            raise ValueError("Meerdere factuurdata op 1 factuur, dat zou niet mogen...")
        factuurdatum = flip_date(factuurdatum[0])

        if consultdatum:
            if len(set(consultdatum)) > 1:  # pragma: no cover
                raise ValueError("Meerdere consultdata op 1 factuur, dat zou niet mogen...")
            consultdatum = flip_date(consultdatum[0])
        else:
            consultdatum = None

        if len(set(betalingsconditie)) > 1:  # pragma: no cover
            raise ValueError(
                "Meerdere betalingscondities op 1 factuur, dat zou ik niet verwachten..."
            )
        betalingsconditie = betalingsconditie[0]

        if len(set(naam)) > 1:  # pragma: no cover
            raise ValueError("Meerdere namen op 1 factuur, dat zou ik niet verwachten...")
        naam = naam[0]

        omschrijving = f"Relatienaam: {naam}\n"
        if consultdatum:
            omschrijving += f"Consultdatum: {consultdatum}\n"
        omschrijving += f"Betalingsconditie: {betalingsconditie}\n"
        if declaratienummer:
            omschrijving += f"Declaratienummer: {declaratienummer}\n"

        mutatie = ebh.models.Mutatie(
            mutatie_nummer="99999",
            soort=ebh.constants.MutatieSoort.factuur_verstuurd,
            datum=factuurdatum,
            rekening=debiteur_rekening,
            relatie_code=relatie,
            factuur_nummer=factuur_nummer,
            omschrijving=omschrijving,
            betalingstermijn="14",
            inclusief_exclusief_btw=ebh.constants.InExBTW.inclusief,
            betalingskenmerk=declaratienummer,
            mutatie_regels=factuurregels,
        )

        facturen.append(mutatie)

    return facturen
