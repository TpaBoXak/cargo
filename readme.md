# Запуск приложения
## Запуск приложения в докере
1. docker-compose -f docker-compose-docker.yaml up
2. Перейти по сслыке в браузере: http://localhost:8000/docs для ознакомления с документацией


## Запуск приложения локально
1. docker-compose -f docker-compose-local.yaml up
2. py -m venv venv
3. Для windows(bash): source ./venv/Scripts/activat
    Для Linux: source ./venv/bin/activat
4. pip install -r requirements.txt
5. poetry install
6. Создание в директории проекта файл .env
7. Пример .env файла:
    APP_CONF__DB__URL = postgresql+asyncpg://Arseniy:12345@127.0.0.1:5434/cargo
    APP_CONF__RUN__HOST = localhost
    APP_CONF__RUN__PORT = 8000
    APP_CONF__KAFKA__BOOTSTRAP_SERVERS=kafka://localhost:9092
    APP_CONF__KAFKA__TOPIC=cargo_logs
8. alembic upgrade head
9. py main.py
10. Перейти по сслыке в браузере: http://localhost:8000/docs для ознакомления с документацией