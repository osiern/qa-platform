FROM python:3.12-slim-bookworm AS app
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY requirements.txt requirements.lock.txt ./
RUN pip install --no-cache-dir -r requirements.lock.txt
COPY shop shop
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. shop/proto/inventory.proto
CMD ["uvicorn", "shop.api:app", "--host", "0.0.0.0", "--port", "8000"]
