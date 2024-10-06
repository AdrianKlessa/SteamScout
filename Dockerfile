FROM python:3.9 AS base
COPY requirements.txt /steam_scout/requirements.txt
RUN pip install -r /steam_scout/requirements.txt

FROM base AS build
COPY . /steam_scout
WORKDIR /steam_scout
RUN python -m src.scripts.docker_prepare_data && rm -f /steam_scout/data/raw/games.csv && rm -f /steam_scout/data/raw/games.json
RUN python -m src.scripts.sqlite_import
RUN python -m src.scripts.vectordb_import  && rm -f /steam_scout/data/processed/games_with_vectors.pickle
RUN python -m src.scripts.sqlite_add_fts

FROM base AS final
COPY --from=build /steam_scout /steam_scout
WORKDIR /steam_scout
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_ANALYTICS_ENABLED="False"
ENV HF_HUB_OFFLINE=1
ENV TRANSFORMERS_OFFLINE=1
ENV DISABLE_TELEMETRY=1
ENV DO_NOT_TRACK=1
ENV HF_HUB_DISABLE_IMPLICIT_TOKEN=1
ENV HF_HUB_DISABLE_TELEMETRY=1
CMD [ "python", "./src/gradio_app.py"]