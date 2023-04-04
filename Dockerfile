FROM python:3.11.2-slim
LABEL author="Dennis Bakhuis"

# copy files and install requirements
COPY requirements.txt pyproject.toml /
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy files
COPY ./voorvoet_app /voorvoet_app

WORKDIR /
EXPOSE 80
CMD ["streamlit", "run", "voorvoet_app/Voorvoet_App.py", "--server.port", "80"]
