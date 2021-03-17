import json
import logging
import boto3
import time
import random

logging.basicConfig(
    format="%(asctime)s %(module)s:%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')

queue_name = 'SampleAppQueue.fifo'

def get_queue_name():
    return queue_name

def get_queue_url(sqs):
    response = sqs.get_queue_url(QueueName=get_queue_name())
    return response['QueueUrl']

def lambda_handler(event, context):
    for record in event['Records']:
        # 長時間かかる場合もあるAPIを呼び出す処理に見立てる
        process_time = random.randint(40, 120)
        logger.info("%d秒かかるAPIコールが発生しています。", process_time)
        time.sleep(process_time)
        # メッセージを削除
        sqs.delete_message(QueueUrl=get_queue_url(sqs), ReceiptHandle=record["receiptHandle"])

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
