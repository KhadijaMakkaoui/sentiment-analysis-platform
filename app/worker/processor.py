import boto3
import os
import time
from textblob import TextBlob

QUEUE_URL = os.getenv('SQS_URL')
REGION = os.getenv('AWS_REGION', 'us-east-1')

sqs = boto3.client('sqs', region_name=REGION)

def process_sentiment(text):
    analysis = TextBlob(text)
    # polarity > 0: Positive, < 0: Negative, == 0: Neutral
    score = analysis.sentiment.polarity
    if score > 0: return "Positive"
    elif score < 0: return "Negative"
    else: return "Neutral"

print("Worker started. Waiting for messages...")

while True:
    # Long polling (waiting up to 20 seconds for a message)
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=20
    )

    messages = response.get('Messages', [])
    for msg in messages:
        text = msg['Body']
        sentiment = process_sentiment(text)
        
        print(f"Processed: '{text}' | Result: {sentiment}")

        # Delete message so it's not processed again
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg['ReceiptHandle']
        )