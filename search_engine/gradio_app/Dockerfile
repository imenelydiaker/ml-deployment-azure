FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application code
COPY app.py client.py ./

# Create non-root user
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 7860

CMD ["python", "app.py"]
