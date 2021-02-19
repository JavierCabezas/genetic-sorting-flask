FROM python:3.7.6-buster as base

RUN mkdir /work/
WORKDIR /work/

COPY ./requirements.txt /work/requirements.txt
RUN pip install -r requirements.txt

COPY ./ /work/
#ENV MYPYPATH=/work/stubs

###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install debugpy

WORKDIR /work/
CMD python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m flask run -h 0.0.0 -p 5000

###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod

CMD flask run -h 0.0.0 -p 5000