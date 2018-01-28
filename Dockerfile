FROM python:3.6-alpine
RUN adduser -D mavki

WORKDIR /home/mavki

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY package package
COPY migrations migrations
COPY mavki.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP mavki.py

RUN chown -R mavki:mavki ./
USER mavki

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]