from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine, app_logger
from app.models import Base
from app.schemas import BookCreate, BookUpdate, BookResponse, KafkaMessage
from app.models import Book
from app.broker.views import broker

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await broker.start()
    app_logger.info("Приложение запущено")
    db = next(get_db())
    try:
        if db.query(Book).count() == 0:
            initial_books = [
                Book(title="Преступление и наказание", author="Федор Достоевский", year=1866, is_available=True),
                Book(title="Война и мир", author="Лев Толстой", year=1869, is_available=False),
                Book(title="Мастер и Маргарита", author="Михаил Булгаков", year=1967, is_available=True),
            ]
            db.add_all(initial_books)
            db.commit()
            app_logger.info("Созданы начальные данные")
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():
    await broker.stop()
    app_logger.info("Приложение остановлено")

@app.get("/books", response_model=List[BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    app_logger.info(f"Создана книга: {db_book.title}")
    return db_book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    update_data = updated_book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)
    
    db.commit()
    db.refresh(book)
    app_logger.info(f"Обновлена книга: {book.title}")
    return book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    title = book.title
    db.delete(book)
    db.commit()
    app_logger.info(f"Удалена книга: {title}")
    return {"message": f"Книга '{title}' удалена"}

@app.get("/books/search/{author}", response_model=List[BookResponse])
def search_books_by_author(author: str, db: Session = Depends(get_db)):
    found_books = db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()
    if not found_books:
        raise HTTPException(status_code=404, detail="Книги данного автора не найдены")
    return found_books


@app.post("/kafka/publish", status_code=202)
async def publish_to_kafka(message: KafkaMessage):
    try:
        await broker.publish(message.model_dump(), topic="in-topic")
        return {"status": "accepted"}
    except Exception as exc:
        app_logger.exception("Ошибка публикации в Kafka")
        raise HTTPException(status_code=500, detail=f"Не удалось отправить сообщение: {exc}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

