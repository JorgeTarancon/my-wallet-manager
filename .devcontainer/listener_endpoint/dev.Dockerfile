FROM python:3.11-slim-bullseye

RUN apt-get update --fix-missing

ENV HOMEDIR=/app
ENV COMPONENT=/listener_endpoint

RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
ENV PYTHONPATH=$PYTHONPATH:/app

COPY . $HOMEDIR

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && cd $HOMEDIR$COMPONENT && poetry install