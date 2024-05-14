FROM python:3.11-slim-bullseye

RUN apt-get update --fix-missing

ENV HOMEDIR=/app
ENV COMPONENT=/listener-endpoint

RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
ENV PYTHONPATH=$PYTHONPATH:/app

COPY $COMPONENT $HOMEDIR$COMPONENT
COPY /config $HOMEDIR/config
COPY /utils $HOMEDIR/utils

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && cd $HOMEDIR$COMPONENT && poetry install

# CHANGE: depending on component
ENTRYPOINT ["python", "listener-endpoint/src/app.py"]