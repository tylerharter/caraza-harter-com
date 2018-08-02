import boto3, zipfile

client = boto3.client('lambda')

def main():
    fname = 'cs301'
    print(client.get_function(FunctionName=fname))

    tmp = 'tmp.zip'
    with zipfile.ZipFile(tmp, 'w') as z:
        z.write('lambdas/cs301/lambda_function.py', '/lambda_function.py')

    with open(tmp, 'rb') as f:
        response = client.update_function_code(FunctionName=fname, ZipFile=f.read())

if __name__ == '__main__':
    main()
