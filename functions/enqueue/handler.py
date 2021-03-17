import logging
import boto3
import datetime
import uuid

logging.basicConfig(
    format="%(asctime)s %(module)s:%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sqs = boto3.client('sqs')
sqsr = boto3.resource('sqs')

queue_name = 'SampleAppQueue.fifo'

def get_queue_name():
    return queue_name

def get_queue_resource():
    return sqsr.get_queue_by_name(QueueName=get_queue_name())

def get_queue_url(sqs):
    response = sqs.get_queue_url(QueueName=get_queue_name())
    return response['QueueUrl']

def lambda_handler(event, context):
    qr = get_queue_resource()
    count_of_message_processed = qr.attributes.get('ApproximateNumberOfMessagesNotVisible')
    logger.info('count of message: %s' % count_of_message_processed)

    date_now = datetime.datetime.now()

    if int(count_of_message_processed) > 0:
        # 処理中のメッセージがあったら何もしない
        logger.info('処理中のメッセージがあります。処理を抜けます。 date: %s' % date_now)
        return
    else:
        # 処理中のメッセージがなかったらエンキューする
        logger.info('処理中のメッセージがありません。処理を続けます。 date: %s' % date_now)
        response = sqs.send_message(
            QueueUrl=get_queue_url(sqs),
            MessageBody="message date : %s" % datetime.datetime.now(),
            MessageGroupId="sampleApp",
            MessageDeduplicationId=str(uuid.uuid4())
        )
        return response
