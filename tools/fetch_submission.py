import boto3, botocore, base64, json, os, sys, base64
from multiprocessing import Pool

BUCKET = 'caraza-harter-cs301'


def main():
    if len(sys.argv) != 3:
        print("Usage: fetch_submission.py <net_id> <proj_id>")
        return

    net_id = sys.argv[1]
    proj_id = sys.argv[2]

    session = boto3.Session(profile_name='cs301ta')
    s3 = session.client('s3')
    response = s3.get_object(Bucket=BUCKET, Key='users/net_id_to_google/%s.txt' % net_id)
    user_id = response['Body'].read()
    print("User ID:", user_id)

    path = 'projects/'+proj_id+'/users/'+str(user_id, 'utf-8')+'/curr.json'
    response = s3.get_object(Bucket=BUCKET, Key=path)
    sub = json.loads(response['Body'].read())

    path = sub["filename"]
    print(path)
    assert(not os.path.exists(path))
    with open(path, 'w') as f:
        code = str(base64.b64decode(sub['payload']), 'utf-8')
        f.write(code)


if __name__ == '__main__':
    main()
