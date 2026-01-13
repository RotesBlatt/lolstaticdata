#!/bin/sh
# Cron job script to check for updates every hour

echo ""
echo "=========================================="
echo "$(date) - Hourly Update Check"
echo "=========================================="
cd /app
python -m lolstaticdata.check_and_update
echo "$(date) - Check completed"
echo "=========================================="
echo ""
