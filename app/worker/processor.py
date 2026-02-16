import boto3
import os
import time
import os
from textblob import TextBlob

print(f"DEBUG: Current Environment Variables: {os.environ}")

QUEUE_URL = os.getenv('SQS_URL')
REGION = os.getenv('AWS_REGION', 'us-east-1')

# Get the endpoint URL (LocalStack) if it exists, otherwise None (Real AWS)
# We use this trick to make the code work both locally and in the Cloud
ENDPOINT_URL = os.getenv('SQS_ENDPOINT_URL') 

sqs = boto3.client(
    'sqs', 
    region_name=REGION,
    endpoint_url=ENDPOINT_URL,  # Add this line
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

if QUEUE_URL is None:
    raise ValueError("ERROR: SQS_URL environment variable is not set!")

def process_sentiment(text):
    analysis = TextBlob(text)
    # polarity > 0: Positive, < 0: Negative, == 0: Neutral
    score = analysis.sentiment.polarity
    if score > 0: return "Positive"
    elif score < 0: return "Negative"
    else: return "Neutral"

print("Worker started. Waiting for queue to be ready...")

while True:
    try:
        # On tente de voir si la queue existe
        sqs.get_queue_attributes(QueueUrl=QUEUE_URL, AttributeNames=['QueueArn'])
        break 
    except Exception:
        print("Queue not found yet, retrying in 2 seconds...")
        time.sleep(2)

print("Queue found! Starting to poll messages...")

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
        print(f"Processed: '{text}' | Result: {sentiment}", flush=True)