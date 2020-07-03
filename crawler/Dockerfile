FROM python:3.8

WORKDIR /app
COPY requirements.txt /app
RUN apt-get update && apt-get install -y --no-install-recommends cron && \
    pip --timeout=1000 install pip --upgrade --disable-pip-version-check && \
    pip --timeout=1000 install -r requirements.txt --disable-pip-version-check

COPY crontab-file /etc/cron.d
RUN chmod u+x /etc/cron.d/crontab-file && crontab /etc/cron.d/crontab-file

COPY . /app

RUN touch /app/file.txt

CMD ["cron", "-f"]