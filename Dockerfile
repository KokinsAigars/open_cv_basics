# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update package list and install OpenCV system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip FIRST, before dealing with requirements
RUN pip install --no-cache-dir --upgrade pip~=26.1.1

# Install JupyterLab directly in the Dockerfile for the development workflow
RUN pip install --no-cache-dir jupyterlab

COPY requirements.txt .

# Install the rest of your packages globally inside the container
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Keep the container running infinitely so you can execute scripts on demand
CMD ["tail", "-f", "/dev/null"]
