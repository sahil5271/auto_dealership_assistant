FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create data directory
RUN mkdir -p data

# Expose API port
EXPOSE 8000

# Default command (text-based)
CMD ["python", "main.py"]

# For API server, use:
# CMD ["python", "main.py", "--api"]

# For voice interaction, use:
# CMD ["python", "main.py", "--voice", "--voice-provider", "local"]
