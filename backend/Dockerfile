# (C) 2025 by OPNLAB Development. All rights reserved.
# Stage 1: Builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install ufw and required tools in the runtime image
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ufw sudo iptables iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Copy only installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
