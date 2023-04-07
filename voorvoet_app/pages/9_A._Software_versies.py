"""Page to track software versions."""
import platform
import streamlit as st
import tomli
import eboekhouden_python as ebh
import pandas as pd
import openpyxl

from footer import footer


with open("pyproject.toml", "rb") as f:
    pyproject = tomli.load(f)
    __version__ = pyproject["tool"]["poetry"]["version"]

st.write("# VoorVoet importeertool 🚀")

st.markdown(
    f"""
    ### Software versies
    - VoorVoet importeertool: {__version__}
    - Python: {platform.python_version()}
    - Streamlit: {st.__version__}
    - Tomli: {tomli.__version__}
    - Eboekhouden-python: {ebh.__version__}
    - Pandas: {pd.__version__}
    - Openpyxl: {openpyxl.__version__}
"""
)

footer()
