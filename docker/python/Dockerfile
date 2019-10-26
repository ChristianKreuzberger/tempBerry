FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /app

COPY requirements*.txt LICENSE /app/
WORKDIR /app

# install requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# copy source code
COPY ./app /app/app

EXPOSE 8000

WORKDIR /app/app

CMD ["gunicorn", "tempBerry.wsgi", "-b 0.0.0.0:8000"]
