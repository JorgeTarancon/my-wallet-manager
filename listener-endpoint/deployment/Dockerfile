FROM python:3.11-slim-bullseye

#ENV DEPENDENCIESTOEXCLUDE=

ENV HOMEDIR=/app
ENV CONFIGDIR=/config

RUN mkdir -p $HOMEDIR
RUN mkdir -p $CONFIGDIR

COPY ./config $CONFIGDIR

WORKDIR $HOMEDIR
COPY ./listener-endpoint $HOMEDIR

ENV PYTHONPATH='$PYTHONPATH:/app'

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install

# CHANGE: depending on component
ENTRYPOINT ["python", "src/app.py"]