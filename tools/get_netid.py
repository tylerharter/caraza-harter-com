import boto3, uuid, os, io, json, mimetypes, git, sys, botocore

BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

def main():
    for user_id in sys.argv[1:]:
        print(get_net_id(user_id))
    
def get_net_id(user_id):
    path = 'users/google_to_net_id/%s.txt' % user_id
    try:
        # extract net_id as plain text
        response = s3.get_object(Bucket=BUCKET, Key=path)
        net_id = response['Body'].read().decode('utf-8')
    except botocore.exceptions.ClientError as e:
        # not linked yet
        if e.response['Error']['Code'] == "NoSuchKey":
            return (200, {"net_id": None})

        # some unexpected error
        raise e

    # verify it points back to this user_id
    try:
        response = s3.get_object(Bucket=BUCKET, Key='users/net_id_to_google/%s.txt' % net_id)
        user_id_check = response['Body'].read().decode('utf-8')
        if user_id != user_id_check:
            return (500, 'google/cs linkage mismatch, please contact your instructor for help (1)')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            return (500, 'google/cs linkage mismatch, please contact your instructor for help (2)')
        # some unexpected error
        raise e

    return (200, {"net_id": net_id})

if __name__ == '__main__':
    main()
