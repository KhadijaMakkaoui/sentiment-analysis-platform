FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Download NLP data
RUN python -m textblob.download_corpora

COPY . .

CMD ["python", "processor.py"]