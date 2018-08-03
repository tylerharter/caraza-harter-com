import json, urllib, boto3, base64
ROUTES = {}
BUCKET = 'caraza-harter-cs301'

# decorator
def route(fn):
    ROUTES[fn.__name__] = fn
    return fn

def get_user(event):
    token = event['GoogleToken']
    req = urllib.request.Request('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+token)
    response = urllib.request.urlopen(req)
    status = json.loads(response.read())
    return status

@route
def answer(user, event):
    s3 = boto3.client('s3')
    user_id = user['sub']
    question_id = event['question_id']
    answer = event['answer']

    entry = {'user_id':user_id, 'answer':answer}
    entryJSON = json.dumps(entry)
    entryB64 = str(base64.b64encode(bytes(entryJSON, 'utf-8')), 'utf-8')
    inlinepath = 'questions/%s/answers/%s' % (question_id, entryB64)

    if len(bytes(inlinepath, 'utf-8')) < 1000:
        path = inlinepath
        s3.put_object(Bucket=BUCKET,
                      Key=inlinepath,
                      Body=bytes(entryJSON, 'utf-8'),
                      ContentType='text/json',
        )
        return (200, {'message': 'answer saved to '+inlinepath})
    else:
        # TODO: save it, but not inline
        return error(500, 'answer too long')

@route
def get_answers(user, event):
    s3 = boto3.client('s3')
    user_id = user['sub']
    question_id = event['question_id']
    path = 'questions/%s/answers' % (question_id)
    answers = []
    files = s3.list_objects(Bucket=BUCKET, Prefix=path, MaxKeys=10000)['Contents']
    for obj in files:
        key = obj['Key']
        name = key.split('/')[-1]
        try:
            b = base64.b64decode(name)
            txt = str(b, 'utf-8')
            row = json.loads(txt)
        except:
            continue
        answers.append(row)
    return (200, {'answers': answers})

def error(message):
    return {
        "isBase64Encoded": False,
        "statusCode": 500,
        "headers": {},
        "body": {'error': message}
    }

def lambda_handler(event, context):
    try:
        user = get_user(event)
    except Exception as e:
        return error('exception thrown during authentication')

    fn = ROUTES.get(event['fn'], None)
    if fn == None:
        return error('no route for '+event['fn'])

    try:
        code, data = fn(user, event)
    except Exception as e:
        return error('Exception: '+str(e))
        
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {},
        "body": data
    }
