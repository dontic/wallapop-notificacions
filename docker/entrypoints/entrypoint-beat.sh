#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

# run celery beat
echo "Starting celery beat..."
celery -A core beat -l info