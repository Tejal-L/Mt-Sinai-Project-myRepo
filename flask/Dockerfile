FROM python:3.6

ENV BEARER_TOKEN=
ENV SLACK_WEBHOOK_SECRET= 

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "receive.py" ]