FROM python:3.13-slim
LABEL author="Dennis Bakhuis"

# copy files and install requirements
COPY requirements.txt pyproject.toml /
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy files
COPY ./voorvoet_app /voorvoet_app

WORKDIR /voorvoet_app
EXPOSE 80
CMD ["streamlit", "run", "Voorvoet_App.py", "--server.port", "80"]
