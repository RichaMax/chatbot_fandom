FROM python:3.13.7

WORKDIR /app

# RUN groupadd --gid 1000 worker && useradd --uid 1000 --gid worker -ms /bin/bash worker
# USER worker
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY pyproject.toml .
COPY uv.lock .

COPY . . 

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8013", "--factory", "backend.app:create_app", "--reload"]
