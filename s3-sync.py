import boto3, uuid, os, io, json, mimetypes, git

# https://s3.us-east-2.amazonaws.com/caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0/index.html

s3 = boto3.client('s3')

def get_web_bucket(search):
    for bucket in s3.list_buckets()['Buckets']:
        name = bucket['Name']
        try:
            tagging = s3.get_bucket_tagging(Bucket=name)
        except Exception as e:
            continue

        tagging = {row['Key']: row['Value'] for row in tagging['TagSet']}
        website = tagging.get('website', None)
        if website:
            if website == search:
                return name

    return None

def get_s3_path(local_base, local_path):
    return os.path.relpath(local_path, local_base)

def get_content_type(path):
    ext = path.split('.')[-1]
    return {
        'htm': 'text/html',
        'html': 'text/html',
    }.get(ext, 'string')

def main():
    repo = git.Repo('.')
    commit = repo.commit()

    subdomain = 'tyler'
    bucket = get_web_bucket('%s.caraza-harter.com' % subdomain)
    assert(bucket)
    print(bucket)

    for dirpath,_,filenames in os.walk(subdomain):
        for filename in filenames:
            local_path = os.path.join(dirpath, filename)
            s3_path = get_s3_path(subdomain, local_path)
            print(local_path, s3_path)
            
            # do upload
            with open(local_path, 'rb') as f:
                ContentType = mimetypes.guess_type(local_path)[0]
                if ContentType == None:
                    ContentType = 'string'
                print(ContentType)
                s3.put_object(Bucket=bucket,
                              Key=s3_path,
                              Body=f,
                              ContentType=ContentType)

    s3.put_object(Bucket=bucket,
                  Key='commit.txt',
                  Body=commit.hexsha,
                  ContentType=ContentType)

if __name__ == '__main__':
    main()
