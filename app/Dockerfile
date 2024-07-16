FROM python:3.10

WORKDIR /project


COPY . .

RUN apt-get update && apt-get -y install cron
COPY crontab /etc/cron.d/main-cron
RUN chmod 0644 /etc/cron.d/main-cron
RUN crontab /etc/cron.d/main-cron
RUN touch /var/log/cron.log

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD cron && tail -f /var/log/cron.log