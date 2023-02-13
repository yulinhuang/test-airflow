# test-airflow

A playground project for exploring software tools for ML pipeline such as airflow.

# Local dev environment installation

Create a conda environment:
```conda create -n mlops python=3.10```
```conda actiavte mlops```


Install the packages with poetry:
```poetry install```

# Launching with docker

Export requirement
```poetry export -f requirements.txt --output requirements.txt --without-hashes```

```docker compose up -d```
or
```docker compose up -d --build``` to keep track of local dag files

