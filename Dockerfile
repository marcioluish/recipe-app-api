FROM python:3.7-alpine

# this environment variable prevents python from buffering outputs
# with this set, it just prints them directly
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
## --update updates the registry of the apk manager
# before a new package is added
## --no-cache prevents storing the registry index on the Dockerfile.
# This minimizes the number of extra files and packages that are
# included in the docker container.
RUN apk add --update --no-cache postgresql-client

## --virtual sets out a alias for the forementioned dependencies.
# This helps us out when cleaning this dependencies later.
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

WORKDIR /app

COPY ./app .

RUN adduser -D user

USER user
