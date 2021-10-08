FROM python:3.7-alpine

# this environment variable prevents python from buffering outputs
# with this set, it just prints them directly
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /app

COPY ./app .

RUN adduser -D user

USER user
