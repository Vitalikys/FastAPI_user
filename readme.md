#  Project to implement main features of FastAPI
[![version](https://img.shields.io/badge/python-3.10-green)](https://semver.org)
[![version](https://img.shields.io/badge/fastapi-0.85.2-green)](https://semver.org)
[![version](https://img.shields.io/badge/SQLAlchemy-1.4.42-yellow)](https://semver.org)
[![version](https://img.shields.io/badge/unittest-latest-blue)](https://semver.org)
[![version](https://img.shields.io/badge/dockerfile-old-red)](https://semver.org)

### Short Functionality Description:
* User (CRUD) 
* Items for this User (create, get all)
* Login User by token
* Two html pages 


## How to run project locally
```shell
git clone https://github.com/Vitalikys/FastAPI_user.git
cd FastAPI_user/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 5000
```
#### create .env file with your data:
```editorconfig
DB_NAME=fastapi_app.db
SECRET_KEY=secret_key_for_password_ABCDEFGHJKLMN
ENDPOINT=http://127.0.0.1:5000
```


#### visit http://localhost:5000/docs

for migrations use:
```shell
alembic upgrade head
```
## How to start project in Docker
#### Build your FastAPI image:
```shell
docker build -t fastapi_users_image .
```

#### Run a container, based on your image:
```shell
docker run -d --name fastapi-users_cont -p 8005:8099 fastapi_users_image
```

## How to Run Tests:  

#### run test for create, get, delete user:
```shell
pytest ./tests/test_user.py -v -s
```