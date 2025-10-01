# Use official Python base image
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY . .

# (Removed USER appuser line — will run as root)

# Expose the port your FastAPI app runs on
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

# Run the app with uvicorn on port 80
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
