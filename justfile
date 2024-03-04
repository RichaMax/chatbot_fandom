set dotenv-load

root := justfile_directory()


@up:
    docker-compose up --force-recreate

@down:
    docker-compose down

ingest *ARGS:
    PYTHONPATH={{root}} {{root}}/ingest/.venv/bin/python ingest {{ARGS}}