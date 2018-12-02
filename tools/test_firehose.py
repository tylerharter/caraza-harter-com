import boto3, botocore, base64, json, os, sys

session = boto3.Session(profile_name='default', region_name='us-east-2')
firehose = boto3.client('firehose')
FIREHOSE_STREAM = 'cs301-trace'

def main():
    print(firehose.list_delivery_streams())
    for i in range(10):
        response = firehose.put_record(DeliveryStreamName=FIREHOSE_STREAM,
                                       Record = {'Data': json.dumps({"test": "pass"})})

    print(response)

if __name__ == '__main__':
    main()
