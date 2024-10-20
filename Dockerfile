FROM python:3.12

WORKDIR /usr/src/app

ADD . .

RUN pip install --no-cache-dir --no-deps -r tg_bot/requirements.txt

CMD ["python", "main.py"]
