#  виносимо константу для хешування паролю в файл ***.env
# from app.config import SECRET_KEY
# SECRET_KEY = config('SECRET_KEY', config)
import hashlib

SECRET_KEY = 'secret'


def get_password_hash(password: str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf8')).hexdigest()
