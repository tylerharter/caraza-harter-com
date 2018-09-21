import boto3, uuid, os, io, json, mimetypes, git, sys, botocore

BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def main():
    for user_id in sys.argv[1:]:
        dump_google_user(user_id)
    
def dump_google_user(user_id):
    path = 'users/google/%s.json' % user_id
    try:
        # extract net_id as plain text
        response = s3.get_object(Bucket=BUCKET, Key=path)
        user = response['Body'].read().decode('utf-8')
        print('='*40)
        print(user_id)
        print(user)
    except botocore.exceptions.ClientError as e:
        # not linked yet
        if e.response['Error']['Code'] == "NoSuchKey":
            print('Missing User')
        raise e

if __name__ == '__main__':
    main()
