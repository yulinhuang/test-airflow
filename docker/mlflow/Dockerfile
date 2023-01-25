FROM python:3.10-bullseye
# USER root
# RUN apt-get update \
#   && apt-get install -y --no-install-recommends \
#          gcc\
#   && apt-get autoremove -yqq --purge \
#   && apt-get clean \
#   && rm -rf /var/lib/apt/lists/*

# USER python

# Install python packages
RUN pip install mlflow

RUN mkdir mlflow

WORKDIR /mlflow