FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY server .
COPY entrypoint.sh .

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
