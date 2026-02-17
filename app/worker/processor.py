import boto3
import json
import os
import time

# 1. Configuration from Environment Variables
# Note: Inside Docker, we use 'localstack' as the hostname
SQS_ENDPOINT = os.getenv("SQS_ENDPOINT_URL", "http://localstack:4566")
DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT_URL", "http://localstack:4566")
REGION = "us-east-1"
QUEUE_URL = os.getenv("SQS_URL")

# 2. Initialize AWS Services with 'test' credentials for LocalStack
# Explicitly providing credentials avoids 'AWS login' or 403 errors
sqs = boto3.client(
    'sqs', 
    endpoint_url=SQS_ENDPOINT, 
    region_name=REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

dynamo = boto3.resource(
    'dynamodb', 
    endpoint_url=DYNAMO_ENDPOINT, 
    region_name=REGION,
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Reference the table created by your init-aws.sh
table = dynamo.Table('SentimentResults')

from textblob import TextBlob

def analyze_sentiment(text):
    # TextBlob calculates polarity: 
    # -1.0 (Very Negative) to 1.0 (Very Positive)
    testimonial = TextBlob(text)
    polarity = testimonial.sentiment.polarity
    
    if polarity > 0.1:
        return "POSITIVE"
    elif polarity < -0.1:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

print("🚀 Worker started. Listening for messages...", flush=True)

while True:
    try:
        # 3. Poll SQS for messages
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=5  # Long polling
        )

        if 'Messages' in response:
            for message in response['Messages']:
                msg_id = message['MessageId']
                body = json.loads(message['Body'])
                text = body.get('text', '')

                print(f"📩 Received: {text}", flush=True)

                # 4. Perform Analysis
                sentiment = analyze_sentiment(text)
                
                # 5. Save Result to DynamoDB
                try:
                    table.put_item(
                        Item={
                            'message_id': msg_id,
                            'text': text,
                            'sentiment': sentiment
                        }
                    )
                    print(f"✅ SUCCESSFULLY stored in DynamoDB: {msg_id} -> {sentiment}", flush=True)
                except Exception as db_err:
                    print(f"❌ DYNAMODB ERROR: {str(db_err)}", flush=True)

                # 6. Delete message from SQS so it isn't processed again
                sqs.delete_message(
                    QueueUrl=QUEUE_URL, 
                    ReceiptHandle=message['ReceiptHandle']
                )
                print(f"🗑️ Deleted message: {msg_id}", flush=True)

    except Exception as e:
        print(f"⚠️ Worker Loop Error: {str(e)}", flush=True)
        time.sleep(2) # Prevent rapid fire error loops