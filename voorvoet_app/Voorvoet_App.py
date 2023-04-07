"""Start page of the streamit app."""
import streamlit as st
from footer import footer

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

    ### Werkwijze importeren bonnentjes Zettle
    1. Ga naar de Zettle website om de mutaties te exporteren. Als je bent ingelogt op de website
    ga naar `stortingen`. In het nieuwe scherm, selecteer de periode die je wilt exporteren. Met
    het dropdown menu transactietype hoef je niets te doen, je downloadt alle types. klik vervolgens
    op `exporteer naar excel`. Sla dit bestand lokaal op met een duidelijke begin en eind datum in
    de naam, bijvoorbeeld `2023-03-01 - 2023-04-01 - Mutaties.xlsx`. Nu weet je dat dit bestand alle
    mutaties van die periode bevat.
    2. In de VoorVoet importeertool ga naar `3. Zettle importeren` en upload het Excel bestand met
    mutaties. Als het bestand goed is geïmporteerd, krijg je het aantal transacties te zien die in
    het bestand staan. Vervolgens wordt vanuit de transacties een lijst met mutaties gemaakt. Dit
    kunnen er meer zijn omdat de transactie 'geld storten op bankrekening' overeen komt met twee
    mutaties in E-boekhouden.nl. Nu wordt er automatisch een overzicht gemaakt van alle mutaties
    die al in E-boekhouden.nl staan en een overzicht van nog toe te voegen mutaties. Kijk even goed
    of dit klopt. Als je akkoord bent, klik dan op de knop `Upload nieuwe mutaties`. Je hebt nu alle
    nieuwe mutaties in E-boekhouden.nl staan.
    3. Alle pinbetalingen zijn geimporteerd als `geld ontvangen` mutaties op rekening 8140. Deze
    hadden eigenlijk `factuurbetaling ontvangen` moeten zijn. Omdat de tool niet automatisch
    de betaling kan koppelen aan de juiste factuur, is dit niet gebeurd. Je moet dit nog handmatig
    doen. In E-boekhouden.nl ga naar `boekhouden`, `overzichten` en dan naar `winst/verliest` en
    zoek naar de Zettle tijdelijk rekening  `8140`. Hier staan alle pinbetalingen. Klik op elke
    pinbetaling en koppel deze aan de juiste factuur. Aan het eind van dit process hoort deze
    tijdelijke rekening leeg te zijn.

    Hopelijk kunnen we in toekomst Zettle vervangen voor een betere pinprovider.

    ### Opmerkingen
    Standaard worden geen records in E-boekhouden overschreven. Bestaande records worden genegeerd maar
    dit wordt tijdens de procedure ook duidelijk aangegeven.
"""
)

footer()
