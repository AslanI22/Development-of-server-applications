from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BookBase(BaseModel):
    """Базовая схема книги"""
    title: str = Field(..., description="Название книги", min_length=1)
    author: str = Field(..., description="Автор книги", min_length=1)
    year: int = Field(..., description="Год издания", ge=1000, le=2100)
    is_available: bool = Field(default=True, description="Доступна ли книга")

class BookCreate(BookBase):
    """Схема для создания книги"""
    pass

class BookUpdate(BaseModel):
    """Схема для обновления книги"""
    title: Optional[str] = Field(None, description="Название книги", min_length=1)
    author: Optional[str] = Field(None, description="Автор книги", min_length=1)
    year: Optional[int] = Field(None, description="Год издания", ge=1000, le=2100)
    is_available: Optional[bool] = Field(None, description="Доступна ли книга")

class BookResponse(BookBase):
    """Схема ответа с книгой"""
    id: int
    
    model_config = ConfigDict(from_attributes=True)  


class KafkaMessage(BaseModel):
    """Схема для сообщения, публикуемого в Kafka"""
    user: str = Field(..., min_length=1, description="Имя пользователя")
    user_id: int = Field(..., ge=1, description="Идентификатор пользователя")

