FROM python:3.7-alpine

# this environment variable prevents python from buffering outputs
# with this set, it just prints them directly
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
##################################### PSYCOPG2 REQUIREMENTS BEFORE PIP INSTALL
## --update updates the registry of the apk manager
# before a new package is added
## --no-cache prevents storing the registry index on the Dockerfile.
# This minimizes the number of extra files and packages that are
# included in the docker container.
RUN apk add --update --no-cache postgresql-client
## --virtual sets out a alias for the forementioned dependencies.
# This helps us out when cleaning this dependencies later.
RUN apk add --update --no-cache --virtual .tmp-psycopg2-deps \
    gcc libc-dev linux-headers postgresql-dev

####################################### PILLOW REQUIREMENTS BEFORE PIP INSTALL
RUN apk add --update --no-cache jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-pillow-deps \
    musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-psycopg2-deps
RUN apk del .tmp-pillow-deps

WORKDIR /app

COPY ./app .

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
# Sets ownership to all directories under "/vol" -> -R (recursive)
RUN chown -R user:user /vol/
## The owner can do everything with the directory and the rest can read
# and execute from the directory
RUN chmod -R 755 /vol/web

USER user
