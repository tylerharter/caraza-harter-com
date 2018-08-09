#!/usr/bin/python
import boto3

def main():
    print('Hello, World!')
    s3 = boto3.client('s3')
    ls = s3.list_objects_v2(Bucket='caraza-harter-cs301', Prefix='', MaxKeys=10000)
    files = []
    while True:
        contents = ls.get('Contents',[])
        files.extend(contents)
        if not 'NextContinuationToken' in ls:
            break
        ls = s3.list_objects_v2(Bucket='caraza-harter-cs301', Prefix='',
                                ContinuationToken=ls['NextContinuationToken'], MaxKeys=10000)

    size = 0
    for f in files:
        print('%.3fKB %s' % (f['Size']/1024.0, f['Key']))
        size += f['Size']
    print('Total: %.3fKB' % (size/1024.0))

if __name__ == '__main__':
    main()
