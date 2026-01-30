# Use official Python slim image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy dependency list first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY main.py .

# Run the bot (default command)
CMD ["python", "main.py"]
