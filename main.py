from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import Term, TermBase, TermUpdate

# Событие старта приложения (автомиграция)
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Glossary API",
    description="API для глоссария терминов",
    version="1.0.0",
    lifespan=lifespan
)

# 1. Получение списка всех терминов
@app.get("/terms/", response_model=List[Term])
def read_terms(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    terms = session.exec(select(Term).offset(offset).limit(limit)).all()
    return terms

# 2. Получение информации о конкретном термине
@app.get("/terms/{key}", response_model=Term)
def read_term(key: str, session: Session = Depends(get_session)):
    term = session.exec(select(Term).where(Term.key == key)).first()
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term

# 3. Добавление нового термина
@app.post("/terms/", response_model=Term)
def create_term(term: TermBase, session: Session = Depends(get_session)):
    # Проверка на дубликат
    existing_term = session.exec(select(Term).where(Term.key == term.key)).first()
    if existing_term:
        raise HTTPException(status_code=400, detail="Term already exists")
    
    db_term = Term.model_validate(term)
    session.add(db_term)
    session.commit()
    session.refresh(db_term)
    return db_term

# 4. Обновление термина
@app.patch("/terms/{key}", response_model=Term)
def update_term(key: str, term_update: TermUpdate, session: Session = Depends(get_session)):
    db_term = session.exec(select(Term).where(Term.key == key)).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    term_data = term_update.model_dump(exclude_unset=True)
    for k, v in term_data.items():
        setattr(db_term, k, v)
        
    session.add(db_term)
    session.commit()
    session.refresh(db_term)
    return db_term

# 5. Удаление термина
@app.delete("/terms/{key}")
def delete_term(key: str, session: Session = Depends(get_session)):
    db_term = session.exec(select(Term).where(Term.key == key)).first()
    if not db_term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    session.delete(db_term)
    session.commit()
    return {"ok": True, "message": "Term deleted"}