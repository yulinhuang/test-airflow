FROM apache/airflow:2.5.1-python3.10

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         gosu git gcc\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

# WORKDIR /tmp

# RUN pip install poetry

# COPY pyproject.toml poetry.lock /tmp/

COPY requirements.txt /tmp/

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN umask 0002; \
    mkdir -p /opt/airflow/notebooks