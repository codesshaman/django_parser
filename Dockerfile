FROM python:alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY app/requirements.txt .

COPY app/project .

RUN pip install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 8000

USER root

CMD python manage.py runserver 0.0.0.0:8000
