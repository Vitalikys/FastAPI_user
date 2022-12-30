from typing import Optional

from pydantic import BaseModel, Field, EmailStr


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
# Now we can make a UserOptional class that will tell FastApi that all the fields are optional.
# Doing it this way cuts down on the duplication of fields
class UserOptional(UserCreate):
    # __annotations__ = {k: Optional[v] for k, v in UserCreate.__annotations__.items()}
    email: Optional[EmailStr] = None
    firstname: Optional[str] = None
class ItemBase(BaseModel):
    title: str #| None = Field(default='title', min_length=3)
    description: str
class ItemCreate(ItemBase):
    pass
    # owner_id: int
