#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

postgres_ready() {
python << END
import sys
import psycopg2
try:
    psycopg2.connect(
        dbname="${DATABASE_NAME}",
        user="${DATABASE_USER}",
        password="${DATABASE_PASSWORD}",
        host="${DATABASE_HOST}",
        port="${DATABASE_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

# Collect static files (e.g., when using whitenoise)
echo "WHITENOISE IS ENABLED - Collecting static files"
python manage.py collectstatic --noinput

echo "Executing $@"
exec "$@"
