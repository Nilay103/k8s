FROM python:3.8.5-slim-buster
USER root

RUN apt-get update \
  && apt-get install \
  && apt-get install -y gcc \
  && apt-get install -y default-libmysqlclient-dev

WORKDIR /server
COPY ./requirements.txt /server
RUN pip install --no-cache-dir -r /server/requirements.txt
COPY . /server

EXPOSE 5000

CMD ["python3", "server.py"]
