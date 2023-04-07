"""3. Zettle importeren page of the streamlit app."""
import sys
import time
from pathlib import Path

import streamlit as st
import eboekhouden_python as ebh

sys.path.append(str(Path(__file__).resolve().parent))
from zettle import (
    zettle_import_from_excel,
    zettle_dataframe_to_mutatie,
    zettle_select_new_mutaties,
    zettle_mutatie_overview,
)

from footer import footer


st.markdown(
    """
    # 3. Zettle importeren 👣
    Hier kan je de Zettle mutaties importeren in E-boekhouden.nl. Dit staat geheel los van
    het importeren van alle facturen en relaties van James.

    Ga naar de Zettle website om de mutaties te exporteren. Als je bent ingelogt op de website
    ga naar `stortingen`. In het nieuwe scherm, selecteer de periode die je wilt exporteren. Met
    het dropdown menu transactietype hoef je niets te doen, je downloadt alle types. klik vervolgens
    op `exporteer naar excel`. Sla dit bestand lokaal op met een duidelijke begin en eind datum in
    de naam, bijvoorbeeld `2023-03-01 - 2023-04-01 - Mutaties.xlsx`. Nu weet je dat dit bestand alle
    mutaties van die periode bevat.

    Upload vervolgens dit Excel bestand hieronder in de importeertool.
"""
)

uploaded_zettle_file = st.file_uploader(
    "Importeer het Zettle Excel facturen bestand",
    type=["xlsx"],
)
if uploaded_zettle_file is not None:
    file_ok, has_new_facturen = False, False
    try:
        zettle_raw_df = zettle_import_from_excel(uploaded_zettle_file)
        zettle_raw = zettle_dataframe_to_mutatie(zettle_raw_df)
        file_ok = True
    except Exception as e:
        st.markdown(
            f"""
            ### Er is iets mis gegaan met het importeren van het Excel bestand.

            Is het bestand wel een Excel bestand? Is het bestand wel een export van Zettle?

            Dit is de foutmelding: {e}
        """
        )

    if file_ok:
        n_mutaties_df = len(zettle_raw_df)  # type: ignore
        st.markdown(
            f"""
            ### Het Zettle stortingen Excel bestand is successvol ingelezen.

            Dit bestand heeft in totaal {n_mutaties_df} mutaties. Nu gaan we kijken of
            er mutatie bij zitten die al in E-boekhouden.nl staan.
        """
        )

        new_mutaties, existing_mutaties = zettle_select_new_mutaties(zettle_raw)  # type: ignore
        if not new_mutaties:
            st.markdown("**Er zijn geen nieuwe mutaties gevonden.**")
        else:
            st.markdown(
                f"**Er zijn in totaal {len(new_mutaties)} mutaties die nog niet in E-boekhouden.nl staan.**"
            )
            has_new_facturen = True

    if has_new_facturen:
        if existing_mutaties:  # type: ignore
            n_existing_mutaties = len(existing_mutaties)
            st.markdown(
                f"""
                ### {n_existing_mutaties} mutaties bestaan al in E-boekhouden.nl en worden **niet** geimporteerd.
                Hier is een overzicht van alle bestaande facturen.
            """
            )
            st.write(zettle_mutatie_overview(existing_mutaties))

        st.markdown(
            """
            ### Nieuwe facturen importeren.
            Hier is een overzicht van alle nieuwe facturen.

            Klik op de `upload` knop om deze nieuwe facturen naar E-boekhouden te importeren.
        """
        )
        st.write(zettle_mutatie_overview(new_mutaties))  # type: ignore

        if st.button("Upload"):
            latest_iteration = st.empty()
            bar = st.progress(0)

            client = ebh.EboekhoudenClient()
            n_facturen = len(new_mutaties)  # type: ignore
            for ix, factuur in enumerate(new_mutaties):  # type: ignore
                client.add_mutatie(mutatie=factuur)
                latest_iteration.text(f"Added {factuur.factuur_nummer}")
                bar.progress((ix + 1) / n_facturen)
                time.sleep(0.2)

            st.markdown(
                """
                ### Alle nieuwe mutaties zijn geimporteerd 🎉
                Ze zijn nu direct zichtbaar in E-boekhouden.nl.

                Alle pinbetalingen zijn geimporteerd als `geld ontvangen` mutaties op rekening 8140. Deze
                hadden eigenlijk `factuurbetaling ontvangen` moeten zijn. Omdat de tool niet automatisch
                de betaling kan koppelen aan de juiste factuur, is dit niet gebeurd. Je moet dit nog handmatig
                doen. In E-boekhouden.nl ga naar `boekhouden`, `overzichten` en dan naar `winst/verliest` en
                zoek naar de Zettle tijdelijk rekening  `8140`. Hier staan alle pinbetalingen. Klik op elke
                pinbetaling en koppel deze aan de juiste factuur. Aan het eind van dit process hoort deze
                tijdelijke rekening leeg te zijn.

                Succes! Hopelijk kunnen we dit in toekomst toch automatiseren.
            """
            )

footer()
