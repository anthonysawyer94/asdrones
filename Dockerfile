FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=asdrones.conf.prod

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/
RUN pip install --no-cache-dir -r /app/requirements/prod.txt

COPY . /app/

RUN chmod +x manage.prod.py

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "asdrones.wsgi.prod:application"]
