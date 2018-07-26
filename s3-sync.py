import boto3, uuid, os, io, json, mimetypes, git

# https://s3.us-east-2.amazonaws.com/caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0/index.html

s3 = boto3.client('s3')

class Syncer:
    def __init__(self):
        self.subdomain = 'tyler' # will be the root directory locally
        self.bucket = self.get_web_bucket('%s.caraza-harter.com' % self.subdomain)
        self.dry = False # dry run
    
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

    def get_last_commit(self):
        response = s3.get_object(Bucket=self.bucket,
                                     Key='commit.txt')
        return response['Body'].read().decode('utf-8')

    def set_last_commit(self, commit):
        s3.put_object(Bucket=self.bucket,
                      Key='commit.txt',
                      Body=commit.encode('utf-8'),
                      ContentType='text/plain')

    def delete_path(self, local_path):
        s3_path = self.get_s3_path(local_path)
        if s3_path.startswith('..'):
            print('SKIP ' + local_path)
            return
        print('DELETE %s' % (s3_path))

        # do upload
        if not self.dry:
            s3.delete_object(Bucket=self.bucket, Key=s3_path)

    def sync_path(self, local_path):
        s3_path = self.get_s3_path(local_path)
        if s3_path.startswith('..'):
            print('SKIP ' + local_path)
            return
        print('%s => %s' % (local_path, s3_path))

        # do upload
        with open(local_path, 'rb') as f:
            ContentType = mimetypes.guess_type(local_path)[0]
            if ContentType == None:
                ContentType = 'string'
            if not self.dry:
                s3.put_object(Bucket=self.bucket,
                              Key=s3_path,
                              Body=f,
                              ContentType=ContentType)

    def sync_all(self):
        for dirpath,_,filenames in os.walk(self.subdomain):
            for filename in filenames:
                local_path = os.path.join(dirpath, filename)
                sync_path(local_path)
        self.set_last_commit(git.Repo('.').commit().hexsha)

    def sync(self):
        repo = git.Repo('.')
        prev = repo.commit(self.get_last_commit())
        curr = repo.commit()
        for d in prev.diff(curr):
            change_type = d.change_type
            print('GIT: %s %s' % (change_type, d.b_path))
            if change_type in ['A', 'M']:
                self.sync_path(d.b_path)
            elif change_type in ['D']:
                self.delete_path(d.b_path)
            else:
                print('Cannot sync mutations of type "%s" yet, please resync all.' % change_type)
        if not self.dry:
            self.set_last_commit(curr.hexsha)

def main():
    Syncer().sync()

if __name__ == '__main__':
    main()
