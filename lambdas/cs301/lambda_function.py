import json, urllib

def get_user(request):
    token = request['google-token']
    req = urllib.request.Request('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+token)
    response = urllib.request.urlopen(req)
    status = json.loads(response.read())
    return status

def lambda_handler(event, context):
    request = json.loads(event['body'])


    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": json.dumps({'status': status}, indent=2)+'\n'
    }
