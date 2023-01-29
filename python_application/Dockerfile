ARG PYTHON_VERSION=3.9-alpine3.8

FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
    alpine-sdk \
    postgresql-dev \
    postgresql-client \
    libpq \
    gettext \
    && apk add --no-cache \
    --upgrade \
    --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing 

WORKDIR /application

COPY . .
RUN pip install -U pip \
    && pip install -r requirements.txt

ENTRYPOINT [ "python" ]

# Expose port 80 for container
EXPOSE 80

# Run application.py file at startup
CMD [ "application.py" ]