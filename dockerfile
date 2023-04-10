FROM python:3.9-slim

WORKDIR /code

COPY . /code

# for setup.py  -setuptools
RUN pip install -e .
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8099"]
# in bash:
# $ docker build -t fastapi_users .    # create image
# $ docker run -d --name mycontainer -p 7777:8099 myimage
# 8099 - only inside container
# 7777 - we open in browser