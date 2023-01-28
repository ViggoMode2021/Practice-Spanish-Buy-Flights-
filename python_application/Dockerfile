FROM python:3.10-slim AS base

# Setup env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

# Dependencies
FROM base AS python-deps

### Install pipenv and compilation dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install -r requirements.txt

# Runtime
FROM gcr.io/distroless/python3

WORKDIR /application
COPY . .

EXPOSE 80
ENTRYPOINT ["python", "application.py"]