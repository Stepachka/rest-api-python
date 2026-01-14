# FastAPI Glossary Service

Сервис глоссария, реализованный на FastAPI с использованием SQLite и Docker.

## Стек технологий
- **FastAPI**: Веб-фреймворк.
- **SQLModel (Pydantic + SQLAlchemy)**: ORM и валидация данных.
- **SQLite**: База данных (файл `glossary.db`).
- **Docker**: Контейнеризация.

## Функциональность
Реализованы все CRUD операции:
1. `GET /terms/` - Список терминов.
2. `POST /terms/` - Создание термина.
3. `GET /terms/{key}` - Поиск термина по ключу.
4. `PATCH /terms/{key}` - Обновление описания.
5. `DELETE /terms/{key}` - Удаление.

## Инструкция по запуску

### 1. Локально
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Docker 
```bash
docker build -t glossary-app .
```
```bash
docker run -p 8000:8000 glossary-app
```