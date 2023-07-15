import boto3
import redis
import os
from datetime import datetime

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
table_name = os.getenv('AWS_DYNAMODB_TABLE_NAME')

aws_session = boto3.Session(
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
dynamodb = aws_session.client('dynamodb')
redis_client = redis.Redis(host='localhost', port=6379)
paging_token = None

while True:
    if paging_token:
        response = dynamodb.scan(TableName=table_name, ExclusiveStartKey=paging_token)
    else:
        response = dynamodb.scan(TableName=table_name)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Caching {len(response['Items'])} items... {paging_token if paging_token else ''}")
    for item in response['Items']:
        key = item['id']['N']
        value = str(item['item']['M'])
        redis_client.set(key, value)
    if 'LastEvaluatedKey' not in response:
        break
    paging_token = response['LastEvaluatedKey']

print('Caching complete!')
