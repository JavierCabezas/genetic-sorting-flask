FROM python:3.7.6-buster as base

RUN mkdir /work/
WORKDIR /work/

COPY requirements.txt /work/requirements.txt
RUN pip install -r requirements.txt

COPY ./ /work/
ENV FLASK_APP=main.py

FROM base as prod
CMD flask run -h 0.0.0 -p 5000