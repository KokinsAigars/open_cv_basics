# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pip FIRST, before dealing with requirements
RUN pip install --no-cache-dir --upgrade pip~=25.1.1

COPY requirements.txt .

# Install the rest of your packages globally inside the container
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Keep the container running infinitely so you can execute scripts on demand
CMD ["tail", "-f", "/dev/null"]
