from flask import Flask, request, jsonify
import boto3
import os


# This is a Flask API. 
# It accepts text and sends it to SQS. 
# For local testing, we'll use an environment variable 
# to toggle between "Local" and "AWS" mode.
app = Flask(__name__)

# Config
QUEUE_NAME = os.getenv('SQS_QUEUE_NAME', 'sentiment-queue')
REGION = os.getenv('AWS_REGION', 'us-east-1')

# Initialize SQS Client
sqs = boto3.client('sqs', region_name=REGION)

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