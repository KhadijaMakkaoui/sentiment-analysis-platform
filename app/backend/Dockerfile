FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (Crucial for Docker caching)
COPY requirements.txt .

# Install the new flask-cors library
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]