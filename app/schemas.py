from typing import Optional

from pydantic import BaseModel, Field, EmailStr
from pydantic import validator


class UserBase(BaseModel):
    firstname: str = Field(default='enter firstname',
                           min_length=3, title='description for FirstName')
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    age: int = Field(default=18, ge=18, le=100,
                     description='Age must be more than 18 and < 100')


class UserLoginForm(BaseModel):
    email: EmailStr
    password: str


class UserOptional(UserCreate):
    """
    class that will tell FastApi that all the fields are optional.
    Doing it this way cuts down on the duplication of fields
    """
    # __annotations__ = {k: Optional[v] for k, v in UserCreate.__annotations__.items()}
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
    age: Optional[int] = None


class ItemBase(BaseModel):
    title: str  # | None = Field(default='title', min_length=3)
    description: str
    count: int = Field(ge=0)

    @validator('count')
    def check_count(cls, value):
        if value < 0 or value > 100:
            raise ValueError('Count items should be between 0...100')

# class ItemCreate(ItemBase):
#     owner_id: int
