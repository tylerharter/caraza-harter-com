import boto3, uuid, os, io, json, mimetypes, git

# https://s3.us-east-2.amazonaws.com/caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0/index.html

s3 = boto3.client('s3')

class Syncer:
    def __init__(self):
        self.subdomain = 'tyler'
        self.bucket = self.get_web_bucket('%s.caraza-harter.com' % self.subdomain)
        print(self.bucket)
    
    def get_web_bucket(self, search):
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

    def get_s3_path(self, local_path):
        return os.path.relpath(local_path, self.subdomain)

    def get_content_type(self, path):
        ext = path.split('.')[-1]
        return {
            'htm': 'text/html',
            'html': 'text/html',
        }.get(ext, 'string')

    def get_last_commit(self):
        response = s3.get_object(Bucket=self.bucket,
                                     Key='commit.txt')
        return response['Body'].read().decode('utf-8')

    def set_last_commit(self, commit):
        s3.put_object(Bucket=self.bucket,
                      Key='commit.txt',
                      Body=commit.encode('utf-8'),
                      ContentType='text/plain')

    def sync_all(self):
        for dirpath,_,filenames in os.walk(self.subdomain):
            for filename in filenames:
                local_path = os.path.join(dirpath, filename)
                s3_path = self.get_s3_path(local_path)
                print(local_path, s3_path)

                # do upload
                with open(local_path, 'rb') as f:
                    ContentType = mimetypes.guess_type(local_path)[0]
                    if ContentType == None:
                        ContentType = 'string'
                    print(ContentType)
                    s3.put_object(Bucket=self.bucket,
                                  Key=s3_path,
                                  Body=f,
                                  ContentType=ContentType)

        self.set_last_commit(git.Repo('.').commit().hexsha)
                    
    def sync(self):
        repo = git.Repo('.')
        prev = repo.commit(self.get_last_commit())
        curr = repo.commit()
        print(prev, curr)

def main():
    Syncer().sync()

if __name__ == '__main__':
    main()
