### Stage 1: Build frontend (Node)
FROM node:20-alpine AS frontend-builder
WORKDIR /build-frontend
COPY frontend/package.json frontend/package-lock.json* ./
COPY frontend/ .
RUN npm ci --silent
# Build static site (Next.js with `output: 'export'` will generate `out/`)
RUN npm run build

### Stage 2: Runtime (Python)
FROM python:3.11-slim
WORKDIR /app

# Install runtime dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy backend source
COPY backend /app/backend

# Copy built static frontend
COPY --from=frontend-builder /build-frontend/out /app/frontend/out

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
