FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set Python path
ENV PYTHONPATH=/app/src

# Expose port
EXPOSE 8000

# Run the MCP Toolbox Server
CMD ["python", "-m", "uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "8000"]
