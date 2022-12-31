# from fastapi_crudrouter import SQLAlchemyCRUDRouter
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


@router.get('/all_users', name='users:list', response_model=list[UserBase])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(connect_db)):
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
    # update_data=user.dict(exclude_unset=True)
    # new_user = User(**update_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'new_user id': new_user.id,
            'New user email Here:': new_user.email,
            'email': new_user.email}


@router.patch('/user/{user_id}', name='Partial update user')
def update_user(user: UserOptional,
                user_id: int,
                db: Session = Depends(connect_db)) -> User:
    user_from_db = db.query(User).filter(User.id == user_id).one_or_none()
    if user_from_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        update_data = user.dict(exclude_unset=True)  # get only fields given to update
        print('update_data', update_data)
        # if 'email' in update_data:
        #     user_from_db.email = update_data['email']
        # if 'firstname' in update_data:
        #     user_from_db.firstname = update_data['firstname']
        # if 'password' in update_data.keys():
        #     user_from_db.password = update_data['password']
        # if 'age' in update_data.keys():
        #     user_from_db.age = update_data['age']

        # user_from_db.save()
        print('user_from_db---', user_from_db.__dict__)
        # updated_user = user_from_db.copy(update=update_data)
        user_from_db.__dict__.update(update_data)
        # user_from_db.update(update_data) # 'User' object has no attribute 'update'
        # user_from_db.save()
        print('updated_user = ', user_from_db.__dict__)
        db.add(user_from_db)
        db.commit()
        db.refresh(user_from_db)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print('=================  got error:')
        print(str(e))
    return user_from_db


"""def update(
        self, db_session: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj"""


@router.get("/user/{user_id}",
            response_model=UserCreate,
            response_model_exclude={"password"})  # скриваємо такі поля
def read_user(user_id: int, db: Session = Depends(connect_db)) -> User:
    db_user = db.query(User).filter(User.id == user_id).one_or_none()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user.__dict__)
    return db_user


@router.get('/items', name='items list')
def all_items(skip: int = 0, limit: int = 100, db: Session = Depends(connect_db)):
    all_item = db.query(Item).all()
    return all_item


@router.post('/user/{user_id}/create_item')
def create_item(user_id: int,
                item: ItemBase = Body(..., embed=True),
                db: Session = Depends(connect_db)):
    """ 'count': None  проблема, не визначає !!! """
    # new_item = Item(description=item.description,
    #                 title=item.title,
    #                 owner_id=user_id,
    #                 count=item.count)
    new_item = Item(**item.dict(), owner_id=user_id)
    print(item.__dict__)
    print(new_item.__dict__)
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
