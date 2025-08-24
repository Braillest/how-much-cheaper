FROM python:3.11

WORKDIR /braillest/src

RUN apt update
RUN apt upgrade -y

RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install matplotlib

ENTRYPOINT sleep infinity
