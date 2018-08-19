import boto3, uuid, os, io, json, mimetypes, git, sys

session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def main():
    # reads

    print('TEST: read to 301 bucket')
    try:
        bucket = 'caraza-harter-cs301'
        response = s3.get_object(Bucket=bucket, Key='users/roster.json')
        print(response['Body'].read())
        print('GOOD')
    except Exception as e:
        print('BAD')
        print(e)

    print('\n\n\n')

    print('TEST: read to other bucket')
    try:
        bucket = 'caraza-harter-logging'
        response = s3.get_object(Bucket=bucket, Key='cs301/AWSLogs/667147198405/CloudTrail/us-east-2/2018/08/11/667147198405_CloudTrail_us-east-2_20180811T1335Z_W3RHo1P3Tj31YNY3.json.gz')
        print(response['Body'].read())
        print('BAD')
    except Exception as e:
        print('GOOD')
        print(e)

    print('\n\n\n')
    # writes

    print('TEST: write to 301 bucket')
    try:
        bucket = 'caraza-harter-cs301'
        s3.put_object(Bucket=bucket,
                      Key='test.txt',
                      Body="test".encode('utf-8'),
                      ContentType='text/plain')
        print('BAD')
    except Exception as e:
        print('GOOD')
        print(e)

    print('\n\n\n')

    print('TEST: write to other bucket')
    try:
        bucket = 'caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0'
        s3.put_object(Bucket=bucket,
                      Key='test.txt',
                      Body="test".encode('utf-8'),
                      ContentType='text/plain')
    except Exception as e:
        print('GOOD')
        print(e)      

if __name__ == '__main__':
    main()
