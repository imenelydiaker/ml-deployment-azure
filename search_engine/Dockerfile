FROM python:3.12-slim AS base

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (layer caching)
COPY pyproject.toml README.md ./

# Copy application code
COPY src/ src/
COPY main.py .

# Re-install so src package is resolved
RUN pip install --no-cache-dir .

# # Create non-root user
# RUN adduser --disabled-password --no-create-home appuser
# USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:3000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]