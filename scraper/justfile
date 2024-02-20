lint:
    - poetry run ruff  --fix .
    - poetry run mypy .

format:
    poetry run ruff format . 

test:
    poetry run pytest tests

parse *ARGS:
    poetry run parse {{ARGS}}

install:
    poetry install
    poetry run mypy --install-types .