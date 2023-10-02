FROM python:3.10-alpine

WORKDIR /usr/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apk update && apk add --no-cache firefox
RUN echo '*/2 5-19 * * * python /usr/app/main.py' | crontab -

CMD ["crond","-f"]