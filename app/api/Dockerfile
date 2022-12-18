FROM python:3.9-slim

ARG RABBIT_MQ_USERNAME=$RABBIT_MQ_USERNAME
ARG RABBIT_MQ_PASSWORD=$RABBIT_MQ_PASSWORD
ARG RABBIT_MQ_URL=$RABBIT_MQ_URL

WORKDIR /api

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "python","-u", "video-consumer.py" ]