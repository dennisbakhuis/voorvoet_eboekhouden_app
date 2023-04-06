"""2. Facturen importeren page of the streamlit app."""
import sys
import time
from pathlib import Path

import streamlit as st
import eboekhouden_python as ebh

sys.path.append(str(Path(__file__).resolve().parent))
from facturen import process_facturen, select_new_facturen, facturen_overview
from footer import footer


st.markdown(
    """
    # 2. Facturen importeren 👣
    Dit is de **tweede** stap van het importeren van relaties en facturen uit het James EPD.

    Relaties importeren is de eerste stap. Als je die nog niet hebt gedaan, ga dan terug naar de
    vorige stap.

    Ga naar het James EPD en exporteer de facturen. Let hierbij op dat je alleen de periode
    nieuwe periode selecteert. Sla dit bestand lokaal op met een duidelijke begin en eind datum in
    de naam, bijvoorbeeld `2023-03-18 - 2023-04-01 - Facturen.xlsx`. Nu weet je dat dit bestand alle
    facturen van die periode bevat.

    Upload vervolgens dit Excel bestand hieronder in de importeertool.
"""
)

uploaded_facturen_file = st.file_uploader(
    "Importeer het James EPD Excel facturen bestand",
    type=["xlsx"],
)
if uploaded_facturen_file is not None:
    file_ok, has_new_facturen = False, False
    facturen_raw = None
    try:
        facturen_raw = process_facturen(uploaded_facturen_file)
        file_ok = True
    except Exception as e:
        st.markdown(
            f"""
            ### Er is iets mis gegaan met het importeren van het Excel bestand.

            Is het bestand wel een Excel bestand? Is het bestand wel een export van het James EPD?

            Dit is de foutmelding: {e}
        """
        )

    if file_ok:
        n_facturen = len(facturen_raw)  # type: ignore
        st.markdown(
            f"""
            ### Het James EPD Excel bestand is successvol ingelezen.

            Dit bestand heeft in totaal {n_facturen} facturen. Nu gaan we kijken of
            er nieuwe facturen bij zijn.
        """
        )

        new_facturen = select_new_facturen(facturen_raw)
        if not new_facturen:
            st.markdown("**Er zijn geen nieuwe facturen gevonden.**")
        else:
            st.markdown(f"**Er zijn {len(new_facturen)} nieuwe facturen gevonden.**")
            has_new_facturen = True

    if has_new_facturen:
        st.markdown(
            """
            ### Nieuwe facturen importeren.
            Hier is een overzicht van alle nieuwe facturen.

            Klik op de `upload` knop om deze nieuwe facturen naar E-boekhouden te importeren.
        """
        )
        st.write(facturen_overview(new_facturen))  # type: ignore
        if st.button("Upload"):
            latest_iteration = st.empty()
            bar = st.progress(0)

            client = ebh.EboekhoudenClient()
            n_facturen = len(new_facturen)  # type: ignore
            for ix, factuur in enumerate(new_facturen):  # type: ignore
                client.add_mutatie(mutatie=factuur)
                latest_iteration.text(f"Added {factuur.factuur_nummer}")
                bar.progress((ix + 1) / n_facturen)
                time.sleep(0.2)

            st.markdown(
                """
                ### Alle nieuwe facturen zijn geimporteerd 🎉
                Ze zijn nu direct zichtbaar in E-boekhouden.nl.
            """
            )

footer()
