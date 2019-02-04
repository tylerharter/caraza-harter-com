import boto3, botocore, base64, json, os, sys
from multiprocessing import Pool

BUCKET = 'caraza-harter-cs301'
SKIP = ['logs/']

# return all S3 objects with the given key prefix, using as many
# requests as necessary
def s3_all_keys(Prefix):
    session = boto3.Session(profile_name='cs301ta')
    s3 = session.client('s3')

    ls = s3.list_objects_v2(Bucket=BUCKET, Prefix=Prefix, MaxKeys=10000)
    keys = []
    while True:
        print('...list_objects...')
        contents = [obj['Key'] for obj in ls.get('Contents',[])]
        keys.extend(contents)
        if not 'NextContinuationToken' in ls:
            break
        ls = s3.list_objects_v2(Bucket='caraza-harter-cs301', Prefix=Prefix,
                                ContinuationToken=ls['NextContinuationToken'],
                                MaxKeys=10000)
    return keys

def chunks(l):
    n = 250
    c = []
    for i in range(0, len(l), n):
        c.append(l[i:i + n])
    return c

def download_chunk(paths):
    session = boto3.Session(profile_name='cs301ta')
    s3 = session.client('s3')

    try:
        for path in paths:
            print('File {}'.format(path))
            local = 'snapshot/' + path
            response = s3.get_object(Bucket=BUCKET, Key=path)
            os.makedirs(os.path.dirname(local), exist_ok=True)
            with open(local, 'wb') as f:
                f.write(response['Body'].read())
    except Exception as e:
        return e
    return None

def main():
    prefix = ""
    if len(sys.argv) == 2:
        prefix = sys.argv[1]

    print('lookup keys')
    paths = s3_all_keys(prefix)

    print('filter based on prefix')
    paths2 = []
    for p in paths:
        include = True
        for skip in SKIP:
            if p.startswith(skip):
                include = False
        if include:
            paths2.append(p)
    paths = paths2
    
    print('chunk keys')
    paths = chunks(paths)

    print('parallel map')
    with Pool(20) as p:
        errors = p.map(download_chunk, paths)

    errors = [e for e in errors if e != None]
    if len(errors) == 0:
        print('no errors')
    else:
        print('ERRORS:')
        for e in errors:
            print(e)

if __name__ == '__main__':
    main()
