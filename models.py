from typing import Optional
from sqlmodel import SQLModel, Field

# Базовая модель Pydantic для валидации входных данных
class TermBase(SQLModel):
    key: str = Field(index=True, unique=True, description="Ключевое слово (термин)")
    description: str = Field(description="Описание термина")

# Модель для базы данных (добавляем ID)
class Term(TermBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# Модель для обновления (поля необязательны)
class TermUpdate(SQLModel):
    key: Optional[str] = None
    description: Optional[str] = None