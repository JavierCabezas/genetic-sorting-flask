FROM python:3.7.4-alpine
RUN apk update
RUN apk add curl

RUN mkdir /work/
WORKDIR /work/
COPY requirements.txt /work/requirements.txt

RUN pip install -r requirements.txt
COPY ./ /work/

ENV FLASK_APP=main.py
ENV FLASK_ENV production
HEALTHCHECK --interval=1m --timeout=10s \
   CMD curl -f http://localhost:5000 || exit 1

EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 main:app