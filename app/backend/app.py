from flask import Flask, request, jsonify
import boto3
import os
from flask_cors import CORS  # Add this

# This is a Flask API. 
# It accepts text and sends it to SQS. 
# For local testing, we'll use an environment variable 
# to toggle between "Local" and "AWS" mode.
app = Flask(__name__)

CORS(app) # This allows your React app to talk to the API

# Config
QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'sentiment-queue')
REGION = os.getenv('AWS_REGION', 'us-east-1')

if QUEUE_NAME is None:
    raise ValueError("ERROR: SQS_NAME environment variable is not set!")
# Initialize SQS Client
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
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Send message to SQS
    try:
        response = sqs.send_message(
            QueueUrl=os.getenv('SQS_URL'),
            MessageBody=text
        )
        return jsonify({"status": "Queued", "message_id": response['MessageId']}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)