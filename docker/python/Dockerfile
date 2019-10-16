FROM python:3.6-slim

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

EXPOSE 8000

WORKDIR /app/app

CMD ["gunicorn", "tempBerry.wsgi", "-b 0.0.0.0:8000"]
