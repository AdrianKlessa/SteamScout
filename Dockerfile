FROM python:3.9 AS base
COPY requirements.txt /steam_scout/requirements.txt
RUN pip install -r /steam_scout/requirements.txt

FROM base AS build
COPY data /steam_scout/data
COPY models /steam_scout/models
COPY src /steam_scout/src
COPY users.json /steam_scout/src/scripts/users.json
WORKDIR /steam_scout
RUN python -m src.scripts.docker_prepare_data && rm -f /steam_scout/data/raw/games.csv && rm -f /steam_scout/data/raw/games.json
RUN python -m src.scripts.sqlite_import
RUN python -m src.scripts.vectordb_import  && rm -f /steam_scout/data/processed/games_with_vectors.pickle
RUN python -m src.scripts.sqlite_add_fts

FROM base AS final
RUN useradd -m appuser
COPY --from=build --chown=appuser:appuser /steam_scout /steam_scout
WORKDIR /steam_scout/src
USER appuser
CMD  gunicorn -w 1 -b 0.0.0.0:${FLASK_PORT} steamscout_flask:app