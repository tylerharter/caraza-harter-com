import boto3, botocore, base64, json, os, sys

BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

# return all S3 objects with the given key prefix, using as many
# requests as necessary
def s3_all_keys(Prefix):
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

def download_submission(project_path):
    # a project path will look something like this:
    # projects/p0/users/115799594197844895033/curr.json

    user_id = project_path.split('/')[-2]
    net_id = lookup_net_id(user_id)
    if net_id == None:
        print('could not lookup NetID for google user_id='+user_id)
        return

    # create user dir for download
    user_dir = os.path.join(SUBMISSIONS, net_id)
    print('download to ' + user_dir)
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)

    # download
    response = s3.get_object(Bucket=BUCKET, Key=project_path)
    submission = json.loads(response['Body'].read().decode('utf-8'))
    file_contents = base64.b64decode(submission.pop('payload'))
    with open(os.path.join(user_dir, submission['filename']), 'wb') as f:
        f.write(file_contents)
    with open(os.path.join(user_dir, 'meta.json'), 'w') as f:
        f.write(json.dumps(submission, indent=2))

def main():
    for i,path in enumerate(s3_all_keys("")):
        print('File {}'.format(i))
        local = 'snapshot/' + path
        if os.path.exists(local):
            continue
        response = s3.get_object(Bucket=BUCKET, Key=path)
        os.makedirs(os.path.dirname(local), exist_ok=True)
        with open(local, 'wb') as f:
            f.write(response['Body'].read())

if __name__ == '__main__':
    main()
