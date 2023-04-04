# VoorVoet Importer tool
This tool is used to import data from James EPD and Zettle into E-boekhouden.nl.

I have made this tool for my wife such that she can easily import data from her EPD
and Zettle into her bookkeeping software.

## Installation and local run
1. Clone the repository
2. Run `conda env create -f environment.yml`
3. Run `conda activate voorvoet_app`
4. Run `poetry install`
5. Run `streamlit run voorvoet_app/voorvoet_app.py`
