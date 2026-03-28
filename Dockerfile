FROM python:3.13-slim
LABEL author="Dennis Bakhuis"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock /
RUN uv sync --frozen --no-dev --no-install-project

COPY ./voorvoet_app /voorvoet_app

WORKDIR /voorvoet_app
EXPOSE 80
CMD ["uv", "run", "streamlit", "run", "Voorvoet_App.py", "--server.port", "80"]
