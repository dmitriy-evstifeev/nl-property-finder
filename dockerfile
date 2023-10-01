FROM python:3.10

WORKDIR /usr/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y --no-install-recommends cron firefox-esr
RUN echo '*/2 5-21 * * * root /usr/local/bin/python /usr/app/main.py > /usr/app/cron.log 2>&1' > /etc/cron.d/scrapper
RUN crontab /etc/cron.d/scrapper

CMD ["cron", "-f"]