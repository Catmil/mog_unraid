# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
RUN pip3 install requests
RUN pip3 install discord
RUN pip3 install pyxivapi
RUN pip3 install python-dotenv
COPY . .
CMD python3 Mog.py
