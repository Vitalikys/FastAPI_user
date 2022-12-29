# from fastapi_crudrouter import SQLAlchemyCRUDRouter
import uuid

from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.database import connect_db
from app.handlers_passw import get_password_hash
from app.models import User, Item, AuthToken
from app.schemas import *

router = APIRouter()


@router.get('/all_users', name='users:list', response_model=list[UserBase])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(connect_db)):
    users = db.query(User).all()
    return users


@router.post('/create_user')
def create_new_user(user: UserCreate = Body(..., embed=True),
                    db: Session = Depends(connect_db)):
    exist_user = db.query(User).filter(User.email == user.email).one_or_none()
    if exist_user:  # try IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered ")
    new_user = User(email=user.email,
                    password=get_password_hash(user.password),
                    firstname=user.firstname,
                    age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'new_user id': new_user.id,
            'New user email Here:': new_user.email,
            'email': new_user.email}


@router.get("/user/{user_id}", response_model=UserBase)
async def read_user(user_id: int, db: Session = Depends(connect_db)):
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    print(db_user.__dict__)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/items', name='items list')
async def all_items(skip: int = 0, limit: int = 100, db: Session = Depends(connect_db)):
    all_item = db.query(Item).all()
    return all_item


@router.post('/user/{user_id}/create_item')
def create_item(user_id: int,
                item: ItemCreate = Body(..., embed=True),
                db: Session = Depends(connect_db)):
    new_item = Item(description=item.description,
                    title=item.title,
                    owner_id=user_id
                    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


# ============================== using TOKEN : ============================================
@router.post('/login', name='user:login')
def login(user_form: UserLoginForm = Body(..., embed=True), db: Session = Depends(connect_db)):
    db_user = db.query(User).filter(User.email == user_form.email).one_or_none()
    if not db_user or get_password_hash(user_form.password) != db_user.password:
        return {'error': 'email/password invalid'}

    auth_token = AuthToken(token=str(uuid.uuid4()), user_id=db_user.id)
    db.add(auth_token)
    db.commit()
    return {'auth token created successfully': auth_token.token}


#  цю функцію можна винести кудись подальше...  ми її використов. для наступної:
def check_auth_token(token: str, db: Session = Depends(connect_db)):
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).one_or_none()
    if auth_token:
        return auth_token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


@router.get('/user_by_token')
def get_user_by_token(token: AuthToken = Depends(check_auth_token), db: Session = Depends(connect_db)):
    user = db.query(User).filter(User.id == token.user_id).one_or_none()
    return {'id': user.id, 'email': user.email}


@router.delete('/user_delete/{user_id}}')
def delete_user(user_id: int, db: Session = Depends(connect_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).one_or_none()
    print('DELETING :', user_to_delete)
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        # Creating OUR own class Response
        # return Response(status="Ok", code="200", message="Success delete user").dict(exclude_none=True)
        return {'message': "Success delete user"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
