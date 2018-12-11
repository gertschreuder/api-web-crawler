FROM ubuntu:18.04
RUN apt-get update -y
FROM python:3.6
ADD . /leadbook
WORKDIR /leadbook
RUN pip3 install -r requirements.txt