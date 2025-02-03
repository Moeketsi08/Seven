FROM python:latest

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# Combine migrations and server start in one command
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000
