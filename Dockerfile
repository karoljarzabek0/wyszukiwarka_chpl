# Use an official Python base image
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-download model into Hugging Face cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sdadas/mmlw-retrieval-roberta-large', trust_remote_code=True)"

COPY . .

EXPOSE 8000

CMD ["gunicorn", "web_app.app:app", "-w", "4", "-b", "0.0.0.0:8000"]