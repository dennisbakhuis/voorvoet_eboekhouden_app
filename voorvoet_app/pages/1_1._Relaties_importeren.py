"""1.1. Relaties importeren page of the streamit app."""
import sys
import time
from pathlib import Path

import streamlit as st
import eboekhouden_python as ebh

sys.path.append(str(Path(__file__).resolve().parent))
from relaties import process_relaties, select_new_relaties, generate_relatie_objects
from footer import footer


st.markdown(
    """
    # 1. Relaties importeren 👣
    Dit is de eerste van het importeren van relaties en facturen uit het James EPD.

    Ga naar het James EPD en exporteer de relaties. Sla dit bestand lokaal op met een duidelijke
    datum in de naam, bijvoorbeeld `2023-04-01 - Relaties.xlsx`. Nu weet je dat dit bestand alle
    relaties van het James EPD tot die datum bevat.

    Upload vervolgens dit Excel bestand hieronder in de importeertool.
"""
)

uploaded_relatie_file = st.file_uploader(
    "Importeer het James EPD Excel relatie bestand",
    type={"xlsx"},
)
if uploaded_relatie_file is not None:
    file_ok, has_new_relaties = False, False
    try:
        relaties_raw = process_relaties(uploaded_relatie_file)
        if relaties_raw.columns.tolist() == [
            "relatie_code",
            "Bedrijf/Naam",
            "Vestigingsadres",
            "Vestigingsadres postcode",
            "Vestigingsadres plaats",
            "Vestigingsadres land",
            "Bedrijf/Particulier",
        ]:
            file_ok = True
        else:
            raise Exception("De kolommen van het Excel bestand kloppen niet.")
    except Exception as e:
        st.markdown(
            f"""
            ### Er is iets mis gegaan met het importeren van het Excel bestand.

            Is het bestand wel een Excel bestand? Is het bestand wel een export van het James EPD?

            Dit is de foutmelding: {e}
        """
        )

    if file_ok:
        st.markdown(
            f"""
            ### Het James EPD Excel bestand is successvol ingelezen.

            Dit bestand heeft in totaal {len(relaties_raw)} relaties. Nu gaan we kijken of
            er nieuwe relaties zijn.
        """
        )

        new_relaties = select_new_relaties(relaties_raw)
        if not new_relaties.empty:
            st.markdown("**Er zijn geen nieuwe relaties gevonden.**")
        else:
            st.markdown(f"**Er zijn {len(new_relaties)} nieuwe relaties gevonden.**")
            has_new_relaties = True

    has_new_relaties = True
    if has_new_relaties:
        st.markdown(
            """
            ### Nieuwe relaties importeren.
            Hier is een overzicht van alle nieuwe relaties.

            Klik op de `upload` knop om deze nieuwe relaties naar E-boekhouden te importeren.
        """
        )
        st.write(new_relaties)
        if st.button("Upload"):
            latest_iteration = st.empty()
            bar = st.progress(0)
            relaties = generate_relatie_objects(new_relaties)

            client = ebh.EboekhoudenClient()
            n_relaties = len(relaties)
            for ix, relatie in enumerate(relaties):
                client.add_relatie(relatie=relatie)
                latest_iteration.text(f"Added {relatie.relatie_code}")
                bar.progress((ix + 1) / n_relaties)
                time.sleep(0.2)

            st.markdown(
                """
                ### Alle nieuwe relaties zijn geimporteerd.
                Ze zijn nu direct zichtbaar in E-boekhouden.nl.
            """
            )

footer()
