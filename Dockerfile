# ── Stage 1: Builder ──────────────────────────────────────
FROM python:3.12-alpine AS builder

WORKDIR /build

# Alpine build dependencies for PostgreSQL and compiling C extensions (like psycopg2)
RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ── Stage 2: Production ──────────────────────────────────
FROM python:3.12-alpine

WORKDIR /app

# Install runtime dependencies only (libpq)
RUN apk add --no-cache libpq

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Run collectstatic, create media directory, then add non-root user and set permissions
RUN python manage.py collectstatic --noinput 2>/dev/null || true && \
    mkdir -p /app/media && \
    addgroup -S app && adduser -S app -G app && \
    chown -R app:app /app

# Switch to non-root user
USER app

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "meditrack.wsgi:application"]
