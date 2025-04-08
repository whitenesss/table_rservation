# 🍽️ Table Reservation API

## 📌 Описание

**Table Reservation API** — RESTful-сервис для управления бронированиями столиков в ресторане. Сервис позволяет создавать, просматривать и удалять брони, а также управлять списком доступных столов.

Проект разработан с использованием **FastAPI**, **PostgreSQL**, **SQLAlchemy (async)** и развёрнут в Docker-среде.

---

## ✅ Функционал

### 📋 Столики (`/tables`)
- `GET /tables/all_tables` — Получить список всех столиков
- `POST /tables/create` — Создать новый столик
- `DELETE /tables/delete/{id}` — Удалить столик по ID

### 🗓️ Брони (`/reservations`)
- `GET /reservations/` — Получить список всех бронирований
- `GET /reservations/{id}` — Получить конкретную бронь по ID
- `GET /reservations/table/{table_id}` — Получить все брони для определённого столика (с фильтрацией по дате)
- `POST /reservations/` — Создать новую бронь
- `DELETE /reservations/{id}` — Удалить бронь

### 🔐 Логика бронирования
- Нельзя создать бронь, если столик уже занят в указанный временной интервал.
- Конфликт бронирования обрабатывается с ошибкой `400 Bad Request`.
- Обработка валидаций осуществляется на уровне API.

---

## ⚙️ Технологии

- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- Docker, Docker Compose
- Pytest

---

## 🚀 Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/whitenesss/table_rservation.git
cd table-reservation
```
2. Запуск 
```bash
chmod +x ./scripts/start_project.sh
```
```bash
./scripts/start_project.sh
```
3. Доступные сервисы:
• FastAPI: http://localhost:8000/docs


### 🗂️ Структура проекта

```plaintext
src/
├── api/               # Роутеры FastAPI (endpoints)
├── crud/              # CRUD-логика
├── models/            # SQLAlchemy-модели
├── schemas/           # Pydantic-схемы
├── database.py        # Подключение и настройка базы данных
├── main.py            # Главная точка входа
├── migrateon/         # Alembic миграции
└── tests/             # Тесты (pytest)
```
### 🧪 Тестирование
```bash
pytest -v   
```