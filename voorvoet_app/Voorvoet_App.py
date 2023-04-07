"""Start page of the streamit app."""
import streamlit as st
from voorvoet_app.footer import footer

st.set_page_config(
    page_title="VoorVoet importeertool",
    page_icon="🚀",
)


st.write("# VoorVoet importeertool 🚀")

st.markdown(
    """
    Dit is een simplele importeertool voor VoorVoet om verschillende exports van andere systemen
    te importeren in E-boekhouden.nl van VoorVoet.

    ### Wat kan deze tool?
    - Relaties importeren vanuit het James EPD via een Excel bestand.
    - Facturen importeren vanuit het James EPD via een Excel bestand.
    - Bonnentjes importeren vanuit Zettle via een Excel bestand.

    Kijk voor de verschillende onderdelen in de sidebar.

    ### Werkwijze importeren relaties en facturen James EPD
    1. Ga naar het James EPD en exporteer de relaties. Sla dit bestand lokaal op met een duidelijke
    datum in de naam, bijvoorbeeld `2023-04-01 - Relaties.xlsx`. Nu weet je dat dit bestand alle
    relaties van het James EPD tot die datum bevat.
    2. In de VoorVoet importeertool ga naar `1. Relaties importeren` en upload het Excel bestand met
    relaties. Als het bestand goed is geïmporteerd, zie je een overzicht van de relaties die in het
    bestand staan en een tabel met alle nieuwe relaties. Als er nieuwe realties zijn, klik dan op de
    knop `Upload nieuwe relaties`. Je hebt nu alle nieuwe relaties in E-boekhouden.nl staan.
    3. Ga naar het James EPD en exporteer de facturen. Let hierbij op dat je alleen de periode
    nieuwe periode selecteert. Sla dit bestand lokaal op met een duidelijke begin en eind datum in
    de naam, bijvoorbeeld `2023-03-18 - 2023-04-01 - Facturen.xlsx`. Nu weet je dat dit bestand alle
    facturen van die periode bevat.
    4. *Voordat je de facturen kan importeren, **moeten** eerst de relaties geimporteerd zijn.* Als'
    dit het geval is ga je naar `2. Facturen importeren` en upload je het Excel bestand met facturen.
    Als het bestand goed is geïmporteerd, zie je een overzicht van de facturen die in het bestand
    staan en een tabel met alle nieuwe facturen. Als er nieuwe facturen zijn, klik dan op de knop
    `Upload nieuwe facturen`. Je hebt nu alle nieuwe facturen in E-boekhouden.nl staan.

    ### Opmerkingen
    Standaard worden geen records in E-boekhouden overschreven. Bestaande records worden genegeerd.
"""
)

footer()
