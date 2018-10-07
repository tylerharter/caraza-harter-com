import boto3, uuid, os, io, json, mimetypes, git, sys, botocore

BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def main():
    for user_id in sys.argv[1:]:
        print(get_net_id(user_id))

def get_net_id(net_id):
    path = 'users/net_id_to_google/%s.txt' % net_id
    response = s3.get_object(Bucket=BUCKET, Key=path)
    google_id = response['Body'].read().decode('utf-8')
    return (200, {"google_id": google_id})

if __name__ == '__main__':
    main()
