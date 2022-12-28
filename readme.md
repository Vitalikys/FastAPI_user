https://fastapi.tiangolo.com/deployment/docker/
#### Build your FastAPI image:
docker build -t fastapi_users_image .


#### Run a container based on your image:
docker run -d --name fastapi-users_cont -p 8005:8099 fastapi_users_image

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8099"]

 8099 - only inside container

 7777 - we open in browser


# FastApi Postgresql CRUD
https://fastapi.tiangolo.com/tutorial/sql-databases/
https://fastapi-crudrouter.awtkns.com/backends/ormar
## How to run

1. uvicorn main:app --reload --port 5000
2. http://127.0.0.1:8000/docs
3. alembic upgrade head  //#migrations 


#####  get one user from DB :
 db_user = db.query(User).filter(User.email == user_form.email).one_or_none()


user_id = Column(Integer, ForeignKey('users.id')) # users.id -TABLENAME

if pydantic.error_wrappers.ValidationError: 2 validation errors for Item
try: title: str | None = Field(default='title', min_length=3)


EMAIL VALIDATOR :
    email: EmailStr
 pip install pydantic[email]


in TESTS
треба видаляти базу
 os.remove('sql_app.db')
 