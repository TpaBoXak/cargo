FROM python:3.11.9-slim

WORKDIR /fastapi

COPY ./start_app.sh /fastapi/start_app.sh
COPY ./app /fastapi/app
COPY ./alembic /fastapi/alembic
COPY ./main.py /fastapi
COPY ./alembic.ini /fastapi
COPY ./config.py /fastapi
COPY ./requirements.txt /fastapi
COPY ./pyproject.toml /fastapi

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN echo "APP_CONF__DB__URL=postgresql+asyncpg://Arseniy:12345@pg:5432/cargo" > /fastapi/.env && \
    echo "APP_CONF__RUN__HOST=0.0.0.0" >> /fastapi/.env && \
    echo "APP_CONF__RUN__PORT=8000" >> /fastapi/.env && \
    echo "APP_CONF__KAFKA__BOOTSTRAP_SERVERS=kafka://kafka:9092" >> /fastapi/.env && \
    echo "APP_CONF__KAFKA__TOPIC=cargo_logs" >> /fastapi/.env


RUN echo "APP_CONF__DB__ECHO=1" > /fastapi/.env.template

RUN chmod +x /fastapi/start_app.sh

ENTRYPOINT ["/fastapi/start_app.sh"]