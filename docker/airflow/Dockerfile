FROM apache/airflow:2.4.1-python3.10

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         gosu git\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow

# WORKDIR /tmp

# RUN pip install poetry

# COPY pyproject.toml poetry.lock* /tmp/

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# RUN pip install --no-cache-dir -r /tmp/requirements.txt


RUN pip install mlflow==1.29.0

RUN pip install scikit-learn

RUN pip install matplotlib



# FROM python:3.10.9

# WORKDIR /code

# COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
