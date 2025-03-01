FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add --no-cache libffi-dev g++ gcc musl-dev \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY main.py decision_tree_model.pkl ./
VOLUME ["/app/data"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]