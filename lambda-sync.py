import boto3, zipfile, os, sys

session = boto3.Session(profile_name='default', region_name='us-east-2')
client = session.client('lambda')

def main():
    fname = 'cs301-test'
    if len(sys.argv) == 2 and sys.argv[1] == 'prod':
        fname = 'cs301'
    print(client.get_function(FunctionName=fname))

    tmp = 'tmp.zip'
    lambda_dirs = ['lambdas/cs301']
    for lambda_dir in lambda_dirs:
        with zipfile.ZipFile(tmp, 'w') as z:
            for name in (n for n in os.listdir(lambda_dir) if n.endswith('.py')):
                z.write(os.path.join(lambda_dir, name), '/'+name)

    with open(tmp, 'rb') as f:
        response = client.update_function_code(FunctionName=fname, ZipFile=f.read())

    os.remove(tmp)

if __name__ == '__main__':
    main()
