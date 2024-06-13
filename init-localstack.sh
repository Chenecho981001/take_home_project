#!/bin/bash
chmod +x init-localstack.sh
awslocal sqs create-queue --queue-name login-queue
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/login-queue --message-body '{
    "user_id": "123",
    "device_type": "mobile",
    "ip": "192.168.1.1",
    "device_id": "device123",
    "locale": "en-US",
    "app_version": 5,
    "create_date": "2023-06-11"}'




