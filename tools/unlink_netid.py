import boto3, uuid, os, io, json, mimetypes, git, sys

BUCKET = 'caraza-harter-cs301'
session = boto3.Session()
s3 = session.client('s3')

def unlink(net_id):
    path1 = 'users/net_id_to_google/%s.txt' % net_id
    response = s3.get_object(Bucket=BUCKET, Key=path1)
    user_id = response['Body'].read().decode('utf-8')
    path2 = 'users/google_to_net_id/%s.txt' % user_id
    print(path1, path2)

    response = s3.delete_objects(
        Bucket=BUCKET,
        Delete={
            'Objects': [
                {'Key': path1},
                {'Key': path2}
            ]
        }
    )
    print(response)

def main():
    for net_id in sys.argv[1:]:
        unlink(net_id)

if __name__ == '__main__':
    main()
