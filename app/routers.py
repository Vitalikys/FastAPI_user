import uuid

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

from app.database import connect_db
from app.handlers_passw import get_password_hash
from app.models import User, Item, AuthToken
from app.schemas import *

router = APIRouter()


@router.get('/all_users',
            name='users:list',
            response_model=list[UserBase],
            response_model_exclude={'items'})
def read_users(db: Session = Depends(connect_db)):
    users = db.query(User).all()
    return users


@router.post('/create_user')
def create_new_user(user: UserCreate = Body(..., embed=True),
                    db: Session = Depends(connect_db)):
    """
    Body(..., embed=True), встановлення ключа user в тілі request body
    """
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
            'New user email:': new_user.email
            }


@router.put('/user/{user_id}', name='Full update user')
def update_user_put(user: UserOptional,
                    user_id: int,
                    db: Session = Depends(connect_db)) -> dict:
    db.query(User).filter(User.id == user_id).update(user.__dict__)
    return {'message': 'The data is updated'}


@router.patch('/user/{user_id}',
              name="partial update user v_2",  # response_model=UserCreate
              )
def upd_user(user: UserOptional,
             user_id: int,
             db: Session = Depends(connect_db)) -> dict:
    """ Updating user Partially,
        empty fields would stay the same
    """
    usr_from_db = db.query(User).filter(User.id == user_id).one_or_none()
    if usr_from_db:
        usr_from_db.email = user.email.lower() or usr_from_db.email
        usr_from_db.firstname = user.firstname or usr_from_db.firstname
        usr_from_db.age = user.age or usr_from_db.age
        db.commit()
        db.refresh(usr_from_db)
        return usr_from_db
    else:
        return {"error": "User not found"}


@router.get("/user/{user_id}",
            response_model=UserCreate,
            response_model_exclude={"password"})  # скриваємо такі поля
def read_user(user_id: int, db: Session = Depends(connect_db)) -> User:
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/items', name='items list', tags=['Items'])
def all_items(db: Session = Depends(connect_db)):
    all_item = db.query(Item).all()
    return all_item


@router.post('/user/{user_id}/create_item' , tags=['Items'])
def create_item(user_id: int,
                item: ItemBase = Body(..., embed=True),
                db: Session = Depends(connect_db)):
    # Check if User with such id exist
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        new_item = Item(**item.dict(), owner_id=user_id)
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except Exception as e:
        raise e


# ============================== using TOKEN : ============================================
@router.post('/login', name='user:login', tags=['With token'])
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
    """

    :param token:
    :param db:
    :return:
    """
    auth_token = db.query(AuthToken).filter(AuthToken.token == token).one_or_none()
    if auth_token:
        return auth_token
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Auth is failed')


@router.get('/user_by_token', tags=['With token'])
def get_user_by_token(token: AuthToken = Depends(check_auth_token), db: Session = Depends(connect_db)):
    user = db.query(User).filter(User.id == token.user_id).one_or_none()
    return {'id': user.id, 'email': user.email}


@router.delete('/user_delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(connect_db)):
    user_to_delete = db.query(User).filter(User.id == user_id).one_or_none()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return {'message': "Success delete user"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
