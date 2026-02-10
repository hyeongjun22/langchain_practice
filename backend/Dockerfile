# python version setting
FROM python:3.11-slim

# work directory setting
WORKDIR /code

# requirements install
COPY ./requirements.txt /code/requirements.txt

# requirements install
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy code 
COPY . /code/backend

# uvicorn run

WORKDIR /code/backend

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port", "8080"]