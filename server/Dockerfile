FROM python:3.11.3-slim-buster

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN mkdir -p /app/app/odoo/temp

EXPOSE 3000

CMD ["python", "main.py"]

USER root