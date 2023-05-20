![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Celery Badge](https://img.shields.io/badge/Celery-37814A?logo=celery&logoColor=fff&style=for-the-badge)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# Описание проекта
Данный проект - это API сервис для парсинга данных об абитуриентах с сайтов университетов. В качестве источников выбраны университеты: АГТУ, ГУЗ, ИЭУП, НГУ им. П. Ф. Лесгафта, МГГЭУ, 
МГТОУ, МХТИ, ОМГУПС, ПСТУ, РГСУ, РГУП, СПбГЭУ, СПБГУ, СПбУТУиЭ, УГТУ.

Стек: `python 3.10`, `FastApi`, `PostgreSQL`, `Redis`, `Celery`, `alembic`, `docker-compose`, `SQLAlchemy`, `dependency-injector`, `beautifulsoup4`, `pdfplumber`, `pandas`, `poetry`

# Содержание
- [Структура проекта](#структура-проекта)
- [Функционал](#функционал)
- [API методы](#api-методы)
- [Модели](#модели)
- [Локальный запуск проекта](#локальный-запуск-проекта)
- [Документация](#документация)

# Структура проекта
- [Api](#api)
- [App](#app)
- [Infrastructure](#infrastructure)
- [Worker](#worker)
- [Корневая директория](#корневая-директория)

## Api
`Директория описывающая работу API.`

`api/auth/` - аутентификация.

`api/auth/auth.py` - бэкенд аутентификации.

`api/auth/manager.py` - менеджер аутентификации.

`api/auth/model.py` - модель User. Поля:

- id - уникальный идентификатор.
- email - почта/логин.
- username - юзернейм.
- registered_at - время регистрации.
- hashed_password - пароль.
- is_active - пользователь активен.
- is_superuser - админ-пользователь.
- is_verified - почта подтверджена.

`api/auth/schemas.py` - схема User модели для чтения и создания юзера.

`api/app.py` - инициализация приложения API, описание эндпоинтов и ивентов.

## App
Директория описывающая работу приложения.

`app/parsers/` - директория с парсерами.

`app/pdf/` - директория с pdf-файлом для парсинга данных с АГТУ.

`app/repository/applicants_repository.py` - репозиторий с запросами к базе данных.

`app/schemas.py` - pydantic-модели. Используются для приведения к модели результатов парсинга.

## Infrastructure
Директория с инфраструктурой проекта.

`infrastructure/redis` - диретория, описывающая работу с redis.

`infrastructure/redis/db.py` - создание сессий для подключения к redis.

`infrastructure/redis/handlers.py` - репозиторий с запросами к redis.

`infrastructure/sql/` - директория для работы с базой данных PostgreSQL.

`infrastructure/sql/migrations/` - директория для работы с alembic.

`infrastructure/sql/migrations/versions/` - список коммитов alembic.

`infrastructure/sql/models/` - директория с моделями базы данных.

`infrastructure/sql/models/applicant.py` - модель абитуриента. Поля:

- id - уникальный идентификатор.
- snils - СНИЛС.
- code - образовательная программа.
- university - университет.
- score - количество баллов.
- origin - подан оригинал.
- position - позиция в списке.
- created_at - дата создания записи.

`infrastructure/sql/config.py` - конфигурация базы данных.

`infrastructure/sql/container.py` - контейнер для работы с базой данных.

`infrastructure/sql/db.py` - создание сессий для подключения к базе данных.

## Worker
Директория описывающая работу очереди задач Celery.

`worker/celery.py` - инициализация приложения Celery, список задач и схема задач, работающих по расписанию.

`worker/celeryconfig.py` - конфигурация приложения Celery.

## Корневая директория

`src/alembic.ini` - конфигурация alembic.

`docker-compose.yml` - конфигурация docker-compose.

`Dockerfile` - конфигурация docker image.

`pyproject.toml` - список пакетов, использующихся в проекте.

# Функционал

Сервис парсит данные об абитуриентах раз в сутки (по умолчанию). Для админа есть возможность изменять период парсинга (`/change_parsing_period`), запускать парсинг принудительно вне очереди (`/force_parsing`).

Реализована регистрация пользователей с помощью JWT-token.

Поиск по критериям доступен для всех пользователей.

Регистрация админа происходит автоматически при запуске FastAPI. 

`Логин` - `abc@abc.abc`

`Пароль` - `123456`

# API методы

- метод поиска данных (по СНИЛС, по программе обучения, по университету);
- метод изменения периода парсинга;
- метод принудительного запуска парсинга;

# Модели

## User

- id - уникальный идентификатор.
- email - почта/логин.
- username - юзернейм.
- registered_at - время регистрации.
- hashed_password - пароль.
- is_active - пользователь активен.
- is_superuser - админ-пользователь.
- is_verified - почта подтверджена.

## Applicant
- id - уникальный идентификатор.
- snils - СНИЛС.
- code - образовательная программа.
- university - университет.
- score - количество баллов.
- origin - подан оригинал.
- position - позиция в списке.
- created_at - дата создания записи.

# Локальный запуск проекта
1. Склонируйте репозиторий.
2. Выполните:
    ```
    > docker-compose up -d --build
    ```
3. Выполните в корневой папке проекта:
    ```
    > make db-generate
    > make db-upgrade
    ```
    Либо выполните внутри контейнера `worker`:
    ```
    > docker container exec -it applicants-worker-1 alembic revision --autogenerate
    > docker container exec -it applicants-worker-1 alembic upgrade head
    ```
4. Проект готов к работе.

# Документация
http://localhost:8000/docs