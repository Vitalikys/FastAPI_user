from setuptools import setup

setup(
    name='app-fastapi-users',
    version='0.1',
    author='Vitalii',
    author_email='vitalik@mail.ua',
    description='Fastapi itvn',
    install_requires=[
        'requests==2.28.1',
        'uvicorn==0.20.0',
        'SQLAlchemy==1.4.42',
        'pytest==7.2',
        'fastapi==0.85.2',
        'email-validator==1.3.0',

        ],
    scripts=['app/main.py']
)