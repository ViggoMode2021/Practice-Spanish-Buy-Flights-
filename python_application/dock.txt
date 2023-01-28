# Python image base
FROM python:3.9

# Run commands to update Linux and install necessary dependencies for psycopg2 (PostgreSQL database adapter for Python)

RUN adduser -D myuser && chown -R myuser /myapp-data \
    apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copy to working directory

WORKDIR /application
COPY . .

# Pip install requirements.txt
RUN pip install -r requirements.
USER myuser
ENTRYPOINT [ "python" ]

# Expose port 80 for container
EXPOSE 80

# Run application.py file at startup
CMD [ "application.py" ]