FROM python:3.12

WORKDIR /app

# RUN groupadd --gid 1000 worker && useradd --uid 1000 --gid worker -ms /bin/bash worker
# USER worker

ENV RYE_HOME="/opt/rye"
ENV PATH="$RYE_HOME/shims:$PATH"

RUN curl -sSf https://rye-up.com/get | RYE_INSTALL_OPTION="--yes" bash

COPY pyproject.toml .
COPY requirements.lock .

RUN rye sync --no-dev

COPY . . 

EXPOSE 8000

CMD ["rye", "run", "start-dev"]