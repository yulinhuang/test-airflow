FROM jupyterhub/jupyterhub

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         git gcc python3-dev\
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install jupyter

RUN useradd -ms /bin/bash airflow

RUN echo 'airflow:airflow' | chpasswd

