FROM python:3.8

RUN pip install -r requirements.txt

RUN mkdir /app

COPY data.py /app/
COPY bot.py /app/
COPY main.py /app/

COPY supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
