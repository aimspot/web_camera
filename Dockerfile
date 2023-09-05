FROM python:3.8

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirements.txt .
RUN pip install -r requirements.txt


COPY data.py .
COPY bot.py .
COPY main.py .

COPY supervisord.conf /etc/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
