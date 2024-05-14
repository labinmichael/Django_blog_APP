
# syntax=docker/dockerfile:1

FROM python:3.9.0

WORKDIR /Django_blog_APP

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]