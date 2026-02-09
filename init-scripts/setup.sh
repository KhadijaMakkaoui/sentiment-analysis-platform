#!/bin/bash
awslocal sqs create-queue --queue-name sentiment-queue
echo "SQS Queue 'sentiment-queue' created successfully!"