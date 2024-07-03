## pull official base image
#FROM python:3.11-slim-buster
#
## set working directory
#WORKDIR /usr/src/app
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
## install system dependencies
#RUN apt-get update \
#  && apt-get -y install netcat gcc postgresql \
#  && apt-get clean
#
## install python dependencies
#RUN pip install --upgrade pip
#COPY ./requirements.txt .
#RUN pip install -r requirements.txt
#
## add app
#COPY . .

FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

