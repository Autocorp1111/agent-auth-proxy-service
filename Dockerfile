FROM python:3.11-slim

WORKDIR /app

# Install system dependencies and Bitwarden CLI
RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    curl \
    gnupg \
    libpq-dev \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @bitwarden/cli@2026.5.0 \
    && rm -rf /var/lib/apt/lists/* /root/.npm

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]