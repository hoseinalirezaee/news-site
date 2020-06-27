FROM python:3.8

WORKDIR /app
COPY ./requirements.txt /app
RUN pip --timeout=1000 install pip --upgrade --disable-pip-version-check && \
    pip --timeout=1000 install -r requirements.txt --disable-pip-version-check

VOLUME /app/statics
EXPOSE 8000

COPY . /app
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]


