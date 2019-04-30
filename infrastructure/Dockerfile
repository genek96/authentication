FROM ubuntu:latest

MAINTAINER Evegeny

RUN apt-get update -y

RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install flask
RUN pip3 install requests

COPY . .
WORKDIR /authentication

EXPOSE 5002

RUN ls

CMD ["flask", "run", "--host=0.0.0.0", "--port=5002"]