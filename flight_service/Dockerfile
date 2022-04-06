FROM python:3.9.6-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc python3-dev musl-dev build-base linux-headers postgresql-dev zlib-dev\
        jpeg-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod a+x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
