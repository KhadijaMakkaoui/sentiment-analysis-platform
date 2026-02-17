import boto3
import os
import json  # <--- VERY IMPORTANT: Ensure this is here
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Environment Variables
# URL should be: http://localstack:4566/000000000000/sentiment-queue
SQS_URL = os.getenv("SQS_URL")
DYNAMO_ENDPOINT = os.getenv("DYNAMO_ENDPOINT_URL", "http://localstack:4566")

# Initialize clients with 'test' credentials
sqs = boto3.client('sqs', 
                   endpoint_url=DYNAMO_ENDPOINT, 
                   region_name='us-east-1',
                   aws_access_key_id='test',
                   aws_secret_access_key='test')

dynamo = boto3.resource('dynamodb', 
                        endpoint_url=DYNAMO_ENDPOINT, 
                        region_name='us-east-1',
                        aws_access_key_id='test',
                        aws_secret_access_key='test')

table = dynamo.Table('SentimentResults')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Send to SQS
        # This is where the 500 usually happens if json isn't imported
        response = sqs.send_message(
            QueueUrl=SQS_URL,
            MessageBody=json.dumps({'text': text})
        )
        
        return jsonify({
            "status": "sent",
            "message_id": response['MessageId']
        }), 200

    except Exception as e:
        # This print will show up in your Docker logs above the 500 error
        print(f"!!! BACKEND ERROR: {str(e)}", flush=True) 
        return jsonify({"error": str(e)}), 500

@app.route('/results/<message_id>', methods=['GET'])
def get_result(message_id):
    try:
        response = table.get_item(Key={'message_id': message_id})
        if 'Item' in response:
            return jsonify(response['Item']), 200
        return jsonify({"status": "processing"}), 202
    except Exception as e:
        print(f"!!! DYNAMO ERROR: {str(e)}", flush=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)