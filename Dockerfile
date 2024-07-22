FROM python:3.9

COPY requirements.txt /steam_scout/requirements.txt
RUN pip install -r /steam_scout/requirements.txt
COPY . /steam_scout
WORKDIR /steam_scout
RUN python -m src.scripts.docker_prepare_data
RUN python -m src.scripts.sqlite_import
RUN python -m src.scripts.vectordb_import
RUN python -m src.scripts.sqlite_add_fts
WORKDIR /steam_scout
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"
CMD [ "python", "./src/gradio_app.py"]