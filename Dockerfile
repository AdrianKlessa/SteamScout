FROM python:3.9 AS base
COPY requirements.txt /steam_scout/requirements.txt
RUN pip install -r /steam_scout/requirements.txt

FROM base AS build
COPY . /steam_scout
WORKDIR /steam_scout
RUN python -m src.scripts.docker_prepare_data && rm /steam_scout/data/raw/games.csv
RUN python -m src.scripts.sqlite_import
RUN python -m src.scripts.vectordb_import  && rm /steam_scout/data/processed/games_with_vectors.pickle
RUN python -m src.scripts.sqlite_add_fts

FROM base AS final
COPY --from=build /steam_scout /steam_scout
WORKDIR /steam_scout
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD [ "python", "./src/gradio_app.py"]