FROM python:3.9.2-alpine3.13

WORKDIR /piazza

COPY . .

RUN python setup.py develop

CMD /bin/sh
