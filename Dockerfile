FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY lolstaticdata/ ./lolstaticdata/
COPY pyproject.toml .

# Create output directory
RUN mkdir -p /app/srv

# Set Python path
ENV PYTHONPATH=/app

# Default command to generate all data
CMD ["sh", "-c", "python -m lolstaticdata.champions && python -m lolstaticdata.items"]
