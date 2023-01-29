ARG PYTHON_VERSION=3.7.0-alpine3.8

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
    alpine-sdk \
    postgresql-dev \
    postgresql-client \
    libpq \
    && apk add --no-cache \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
    && pip install --upgrade pip

RUN adduser -D worker

USER worker

WORKDIR /home/worker

COPY --chown=worker:worker requirements.txt requirements.txt

RUN pip install --user -r requirements.txt

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker . .

ENTRYPOINT [ "python" ]

# Expose port 80 for container
EXPOSE 80

# Run application.py file at startup
CMD [ "application.py" ]