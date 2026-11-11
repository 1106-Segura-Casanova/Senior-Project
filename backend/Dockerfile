 # 1. Use Python as the container's operating environment
FROM python:3.14-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy backend dependencies
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the backend application into the container

COPY app/ ./app/

# 6. Copy Alembic migration configuration and scripts

COPY alembic.ini .
COPY migrations/ ./migrations/

# 7. Configure Python output

ENV PYTHONUNBUFFERED=1

# 8. Start FastAPI using the port provided by Cloud Run

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]

