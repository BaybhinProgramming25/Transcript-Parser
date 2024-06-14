FROM python:3.11.1

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt 

RUN pip install -r /backend/requirements.txt 

COPY ./tparser/src/backend /backend/tparser 