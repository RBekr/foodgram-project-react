FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libcairo2-dev \
    libgirepository1.0-dev

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .


CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ] 