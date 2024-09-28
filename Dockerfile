FROM debian:12-slim AS build

RUN apt-get update \
    && apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m venv /venv \
    && /venv/bin/pip install --upgrade pip

FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install -r /requirements.txt

FROM gcr.io/distroless/python3-debian12:nonroot

WORKDIR /app
COPY --from=build-venv /venv /venv
COPY main.py /app/main.py

ENTRYPOINT ["python", "main.py"]
