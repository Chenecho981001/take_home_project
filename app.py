import boto3
import hashlib
import json
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime


# AWS SQS Client Configuration
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
queue_url = 'http://localhost:4566/000000000000/login-queue'

# Postgres Configuration
DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/postgres'
engine = create_engine(DATABASE_URI)
metadata = MetaData()
user_logins = Table('user_logins', metadata,
                    Column('user_id', String),
                    Column('device_type', String),
                    Column('masked_ip', String),
                    Column('masked_device_id', String),
                    Column('locale', String),
                    Column('app_version', Integer),
                    Column('create_date', Date))
metadata.create_all(engine)


# Function to mask PII
def mask_pii(value):
    return hashlib.sha256(value.encode()).hexdigest()


# Read messages from SQS and process
def process_messages():
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)

    if 'Messages' in response:
        for message in response['Messages']:
            data = json.loads(message['Body'])
            user_login = {
                'user_id': data['user_id'],
                'device_type': data['device_type'],
                'masked_ip': mask_pii(data['ip']),
                'masked_device_id': mask_pii(data['device_id']),
                'locale': data['locale'],
                'app_version': data['app_version'],
                'create_date': datetime.strptime(data['create_date'], '%Y-%m-%d').date()
            }

            insert_stmt = insert(user_logins).values(user_login).on_conflict_do_nothing()

            with engine.connect() as conn:
                conn.execute(insert_stmt)

            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])


if __name__ == "__main__":
    process_messages()
