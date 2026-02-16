FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FIX: Specifically call the module correctly
RUN python -m textblob.download_corpora

COPY . .

CMD ["python", "processor.py"]