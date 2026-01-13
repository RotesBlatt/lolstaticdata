FROM python:3.12-slim

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY lolstaticdata/ ./lolstaticdata/
COPY pyproject.toml .

# Copy cron script
COPY check_updates.sh /app/check_updates.sh
RUN sed -i 's/\r$//' /app/check_updates.sh && chmod +x /app/check_updates.sh

# Create output directory and log file
RUN mkdir -p /app/srv && touch /var/log/cron.log

# Set Python path
ENV PYTHONPATH=/app

# Setup cron job to run the update checker every hour
RUN echo "0 * * * * root /app/check_updates.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/update-checker && \
    chmod 0644 /etc/cron.d/update-checker

# Create startup script that runs initial generation and starts cron
RUN echo '#!/bin/sh\n\
echo "==========================================="\n\
echo "Starting LOL Static Data Generator"\n\
echo "==========================================="\n\
echo ""\n\
echo "Running initial data generation..."\n\
python3 -m lolstaticdata.check_and_update\n\
echo ""\n\
echo "Initial generation complete!"\n\
echo "Starting cron daemon for hourly updates..."\n\
cron\n\
echo "Cron started successfully."\n\
echo "Monitoring update logs..."\n\
echo "==========================================="\n\
tail -f /var/log/cron.log' > /app/start.sh && chmod +x /app/start.sh

# Default command: run initial generation and start cron daemon
CMD ["/app/start.sh"]
