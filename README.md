# Applicants

## Описание проекта
`applicants` - это API сервис для парсинга данных об абитуриентах с сайтов университетов. В качестве источников выбраны университеты: АГТУ, ГУЗ, ИЭУП, НГУ им. П. Ф. Лесгафта, МГГЭУ, 
МГТОУ, МХТИ, ОМГУПС, ПСТУ, РГСУ, РГУП, СПбГЭУ, СПБГУ, СПбУТУиЭ, УГТУ.

Стек: `python 3.10`, `FastApi`, `PostgreSQL`, `Redis`, `Celery`, `alembic`, `docker-compose`, `SQLAlchemy`, `dependency-injector`, `beautifulsoup4`, `pdfplumber`, `pandas`, `poetry`

## Функционал

Сервис парсит данные об абитуриентах раз в сутки (по умолчанию). Для админа есть возможность изменять период парсинга (`/change_parsing_period`), запускать парсинг принудительно вне очереди (`/force_parsing`).

Реализована регистрация пользователей с помощью JWT-token.

Поиск по критериям доступен для всех пользователей.

Регистрация админа происходит автоматически при запуске FastAPI. 

`Логин` | `пароль` - `abc@abc.abc` |  `123456`

### API методы

- метод поиска данных (по СНИЛС, по программе обучения, по университету);
- метод изменения периода парсинга;
- метод принудительного запуска парсинга;

## Модели

### User
### Applicant
- snils (СНИЛС)
- code (Направление обучения)
- university (Университет)
- score (Количество баллов)
- origin (Подан оригинал)
- position (Позиция в списке)

## Документация
http://localhost:8000/docs


## Запуск проекта
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