from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "glossary.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False нужен только для SQLite
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Автоматическая миграция: создает таблицы, если их нет"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Зависимость для получения сессии БД"""
    with Session(engine) as session:
        yield session