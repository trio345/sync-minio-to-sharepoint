# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base
WORKDIR /app

# Builder stage: install dependencies in a venv
FROM base AS builder

# Copy only requirements.txt first for better caching
COPY --link requirements.txt ./

# Create virtual environment and install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt && \ 
    .venv/bin/pip install cryptography

# Copy any other .py files in the root (if needed)
COPY --link *.py ./

# Final stage: minimal runtime image
FROM base AS final

# Create a non-root user
RUN useradd -m appuser
USER appuser

WORKDIR /app

# Copy app code and venv from builder
COPY --from=builder --link /app /app
COPY --from=builder --link /app/.venv /app/.venv

# Activate venv for all commands
ENV PATH="/app/.venv/bin:$PATH"

# Default command (adjust if main.py is not the entrypoint)
CMD ["python", "main.py"]
