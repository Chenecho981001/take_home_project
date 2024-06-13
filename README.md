# User Login Processor

## Overview
This application reads JSON data from an AWS SQS Queue, masks PII fields, and writes the transformed data to a Postgres database.

## Setup

### Prerequisites
- Docker
- Docker Compose
- Python 3.8+


### Running the Application

1. Start Docker services:
    docker-compose up -d

2. Initialize LocalStack:
    ./init-localstack.sh

3. Run the application:
    python app.py
    

### Production Considerations

1. **Deployment**: Deploy using container orchestration tools like Kubernetes or ECS. 
2. **Error Handling**: Implement robust error handling and logging mechanisms.
3. **Scalability**: Use SQS message batching, increase SQS visibility timeout, and use worker nodes to process messages in parallel.
4. **PII Recovery**: Store the original PII in a secure, encrypted data store if recovery is needed, with strict access controls.
5. **Assumptions**:
   - The SQS queue and Postgres database schemas are correctly set up.
   - The network setup allows connectivity between the services.
   - Masking is done using SHA-256 for simplicity and consistency.

## License
MIT
