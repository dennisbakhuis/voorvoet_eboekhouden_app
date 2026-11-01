"""Process facturen from Excel file to e-Boekhouden format."""

import datetime
from typing import BinaryIO

import eboekhouden_python as ebh
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

btw_codes = {
    0: ebh.constants.BtwCode.geen,
    0.21: ebh.constants.BtwCode.hoog_verkoop_21,
    0.09: ebh.constants.BtwCode.laag_verkoop_9,
}


def flip_date(date):
    """Convert date to YYYY-MM-DD string."""
    if isinstance(date, str):
        return datetime.datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
    return pd.Timestamp(date).strftime("%Y-%m-%d")


def process_facturen(
    uploaded_file: UploadedFile | BinaryIO,
    prefix_factuur: str = "JF-",
    prefix_relatie: str = "JR-",
    debiteur_rekening: str = "1300",
):
    """Process facturen from Excel file to e-Boekhouden format."""
    facturen_raw = pd.read_excel(uploaded_file, header=3)

    verwachte_kolommen = {
        "Debiteurennummer",
        "Factuurnummer",
        "Declaratienummer",
        "Naam",
        "Factuurdatum",
        "Consult datum",
        "Beschrijving",
        "Betalingsconditie",
        "Grootboekrekening omzet",
        "Bedrag",
        "BTW code",
    }
    ontbrekend = verwachte_kolommen - set(facturen_raw.columns)
    if ontbrekend:
        raise ValueError(
            f"Dit is geen geldig James EPD facturen bestand. "
            f"De volgende kolommen ontbreken: {', '.join(sorted(ontbrekend))}. "
            f"Controleer of je het juiste bestand hebt geüpload op de juiste pagina."
        )

    facturen_raw["Declaratienummer"] = facturen_raw["Declaratienummer"].apply(
        lambda x: str(int(x)) if pd.notna(x) else None,
    )
    facturen_raw["Consult datum"] = facturen_raw["Consult datum"].apply(
        lambda x: x if pd.notna(x) else None,
    )
    facturen = []
    for factuur_nummer_original, factuurregels_raw in facturen_raw.groupby(
        "Factuurnummer"
    ):
        factuur_nummer = f"{prefix_factuur}{factuur_nummer_original}"
        factuurregels, relatie, declaratienummer = [], [], []
        factuurdatum, consultdatum = [], []
        omschrijvingen, betalingsconditie, naam = [], [], []

        for _, regel in factuurregels_raw.iterrows():
            btw_code = btw_codes.get(regel["BTW code"])
            if btw_code is None:
                raise ValueError(f"Onbekende BTW code: {regel['BTW code']}")
            factuurregels.append(
                ebh.models.MutatieRegel.from_bedrag(
                    bedrag_invoer=regel.Bedrag,
                    btw_code=btw_code,
                    tegenrekening_code=regel["Grootboekrekening omzet"],
                )
            )

            relatie.append(regel.Debiteurennummer)
            if pd.notna(regel.Declaratienummer) and regel.Declaratienummer:
                declaratienummer.append(regel.Declaratienummer)

            factuurdatum.append(regel.Factuurdatum)

            if pd.notna(regel["Consult datum"]) and regel["Consult datum"]:
                consultdatum.append(regel["Consult datum"])

            if regel["Beschrijving"]:
                omschrijvingen.append(regel["Beschrijving"])

            if regel["Betalingsconditie"]:
                betalingsconditie.append(regel["Betalingsconditie"])

            if regel["Naam"]:
                naam.append(regel["Naam"])

        if len(set(relatie)) > 1:  # pragma: no cover
            raise ValueError("Meerdere relaties, dat zou niet mogen...")
        relatie_code = f"{prefix_relatie}{relatie[0]}"

        declaratie: str | None = None
        if declaratienummer:
            if len(set(declaratienummer)) > 1:  # pragma: no cover
                raise ValueError("Meerdere declaratienummers, dat zou niet mogen...")
            declaratie = str(int(declaratienummer[0]))

        if len(set(factuurdatum)) > 1:  # pragma: no cover
            raise ValueError("Meerdere factuurdata op 1 factuur, dat zou niet mogen...")
        datum = flip_date(factuurdatum[0])

        consult: str | None = None
        if consultdatum:
            if len(set(consultdatum)) > 1:  # pragma: no cover
                raise ValueError(
                    "Meerdere consultdata op 1 factuur, dat zou niet mogen..."
                )
            consult = flip_date(consultdatum[0])

        if len(set(betalingsconditie)) > 1:  # pragma: no cover
            raise ValueError(
                "Meerdere betalingscondities op 1 factuur, dat zou ik niet verwachten..."
            )
        conditie = betalingsconditie[0] if betalingsconditie else "Onbekend"

        if len(set(naam)) > 1:  # pragma: no cover
            raise ValueError(
                "Meerdere namen op 1 factuur, dat zou ik niet verwachten..."
            )
        relatie_naam = naam[0] if naam else "Onbekend"

        omschrijving = f"Relatienaam: {relatie_naam}\n"
        if consult:
            omschrijving += f"Consultdatum: {consult}\n"
        omschrijving += f"Betalingsconditie: {conditie}\n"
        if declaratie:
            omschrijving += f"Declaratienummer: {declaratie}\n"

        mutatie = ebh.models.Mutatie(
            mutatie_nummer="99999",
            soort=ebh.constants.MutatieSoort.factuur_verstuurd,
            datum=datum,
            rekening=debiteur_rekening,
            relatie_code=relatie_code,
            factuur_nummer=factuur_nummer,
            omschrijving=omschrijving,
            betalingstermijn="14",
            inclusief_exclusief_btw=ebh.constants.InExBTW.inclusief,
            betalingskenmerk=declaratie,
            mutatie_regels=factuurregels,
        )

        facturen.append(mutatie)

    return facturen
