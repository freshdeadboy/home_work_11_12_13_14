from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime, date
from src.dto.user import UserResponse

class ContactSchema(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    last_name: str = Field(min_length=3, max_length=20)
    email: Optional[EmailStr]
    phone: int
    birthday: str

class ContactUpdateSchema(ContactSchema):
    name: str = Field(min_length=3, max_length=20)
    last_name: str = Field(min_length=3, max_length=20)
    email: Optional[EmailStr]
    phone: int
    birthday: str

class ContactResponse(BaseModel):
    id: int = 1
    name: str
    last_name: str
    email: Optional[str]
    phone: int
    birthday: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None

    model_config = ConfigDict(from_attributes = True)


