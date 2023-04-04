# VoorVoet James EPD -> E-boekhouden.nl importer tool
This tool is used to import data from James EPD and Zettle into E-boekhouden.nl.

I have made this tool for my wife such that she can easily import data from her EPD
and Zettle into her bookkeeping software.

![Screenshot of the main app.](https://github.com/dennisbakhuis/voorvoet_eboekhouden_app/blob/main/assets/screenshot1.png?raw=true)

## Installation and local run
1. Clone the repository
2. Run `conda env create -f environment.yml`
3. Run `conda activate voorvoet_app`
4. Run `poetry install`
5. Run `streamlit run voorvoet_app/voorvoet_app.py`

## Run using Docker
```bash
docker run --rm -d \
  -e EBOEKHOUDEN_USERNAME=eboekhouden_username \
  -e EBOEKHOUDEN_CODE1=eboekhouden_code1 \
  -e EBOEKHOUDEN_CODE2=eboekhouden_code2 \
  dennisbakhuis/voorvoer_eboekhouden_app:latest
```

## Create your own deployment
You might want to change your docker hub username in the `Makefile`.
```bash
make docker
```
