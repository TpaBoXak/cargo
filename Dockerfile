FROM python:3.11-slim

WORKDIR /fastapi

COPY ./app /fastapi/app
COPY ./alembic /fastapi/alembic
COPY ./main.py /fastapi
COPY ./alembic.ini /fastapi
COPY ./config.py /fastapi
COPY ./requirements.txt /fastapi
COPY ./start.sh /fastapi
COPY ./pyproject.toml /fastapi


RUN pip install --no-cache-dir -r /fastapi/requirements.txt

RUN echo "APP_CONF__DB__URL=postgresql+asyncpg://Arseniy:12345@pg:5432/cargo" > /fastapi/.env && \
    echo "APP_CONF__RUN__HOST=0.0.0.0" >> /fastapi/.env && \
    echo "APP_CONF__RUN__PORT=8000" >> /fastapi/.env


RUN echo "APP_CONF__DB__ECHO=1" > /fastapi/.env.template

RUN chmod +x /fastapi/start.sh

CMD ["/fastapi/start.sh"]