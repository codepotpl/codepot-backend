FROM python:3.4.3-slim

RUN ["apt-get", "update", "--fix-missing"]
RUN ["pip", "install", "--upgrade", "pip"]
RUN ["apt-get", "install", "-y", "build-essential"]
RUN ["apt-get", "install", "-y", "python3.4-dev"]
RUN ["apt-get", "install", "-y", "libpq-dev"]

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN ["pip", "install", "-r", "requirements.txt"]

ADD . /app
ADD . /log

EXPOSE 8080

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]