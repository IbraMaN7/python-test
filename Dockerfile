FROM python:3.9 

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /app/
RUN chmod +x /app/docker-entrypoint.sh
COPY . /app/
