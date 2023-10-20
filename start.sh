#!/bin/bash
cd /app/plasticome/config && celery -A celery_config worker -l info --pool=solo &
cd /app && task run