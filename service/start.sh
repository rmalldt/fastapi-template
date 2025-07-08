#!/bin/bash
set -e

# Load environment variables from service.env
source /home/rupeshmall/apps/fastapi-template/service/service.env

# Load any additional app specific .env file if it exists
if [ -f /home/rupeshmall/apps/fastapi-template/.env ]; then
	source /home/rupeshmall/apps/fastapi-template/.env
fi

# Start gunicorn using the environment variables
exec "${VIRTUAL_ENV}/bin/gunicorn" \
	-w "${WORKERS}" \
	-k "${WORKER_CLASS}" \
	"${APP_MODULE}" \
	--bind "${HOST}":"${PORT}" \
	--log-level "${LOG_LEVEL}"
