FROM python:3.6-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir /app
WORKDIR /app

# first copy requirements, readme and license file
COPY requirements /app/requirements
COPY requirements.txt README.md LICENSE /app/

# install requirements
RUN pip install --no-cache-dir -r requirements/base.txt
RUN pip install --no-cache-dir -r requirements/production.txt

# now copy the source code
COPY ./app /app/app

EXPOSE 8000

WORKDIR /app/app

CMD ["gunicorn", "tempBerry.wsgi", "-b 0.0.0.0:8000"]
