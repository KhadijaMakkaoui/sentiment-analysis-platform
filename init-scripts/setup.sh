#!/bin/bash
# awslocal sqs create-queue --queue-name sentiment-queue
# echo "SQS Queue 'sentiment-queue' created successfully!"

#!/bin/bash

# Create SQS Queue
awslocal sqs create-queue --queue-name sentiment-queue

# Create DynamoDB Table
awslocal dynamodb create-table \
    --table-name SentimentResults \
    --attribute-definitions AttributeName=message_id,AttributeType=S \
    --key-schema AttributeName=message_id,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "AWS Local Resources Initialized!"

