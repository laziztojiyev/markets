FROM python:alpine
WORKDIR /app
COPY . /app


CMD ["python3", "manage.py"]