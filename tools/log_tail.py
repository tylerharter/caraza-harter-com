import boto3, botocore, base64, json, os, sys, datetime, gzip
from multiprocessing import Pool

BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')
        
# return all S3 objects with the given key prefix, using as many
# requests as necessary
def s3_all_keys(Prefix):
    session = boto3.Session(profile_name='cs301ta')

    ls = s3.list_objects_v2(Bucket=BUCKET, Prefix=Prefix, MaxKeys=10000)
    keys = []
    while True:
        contents = [obj['Key'] for obj in ls.get('Contents',[])]
        keys.extend(contents)
        if not 'NextContinuationToken' in ls:
            break
        ls = s3.list_objects_v2(Bucket='caraza-harter-cs301', Prefix=Prefix,
                                ContinuationToken=ls['NextContinuationToken'],
                                MaxKeys=10000)
    return keys

def main():
    now = datetime.datetime.now()
    prefix = 'logs/kinesis%d/%02d/%02d' % (now.year, now.month, now.day)
    paths = s3_all_keys(prefix)
    paths.sort()
    for path in paths:
        response = s3.get_object(Bucket=BUCKET, Key=path)
        g = gzip.GzipFile(fileobj=response['Body'])
        print(g.read())

if __name__ == '__main__':
    main()
