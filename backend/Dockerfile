# Use full python:3.11 image which includes gcc and build tools
# This avoids Debian repository hash mismatch issues
FROM python:3.11

WORKDIR /app

# Copy requirements (no system packages needed - psycopg2-binary is self-contained)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for uploads and vector store
RUN mkdir -p /app/uploads /app/vector_store

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
