import json, urllib, boto3, botocore, base64, time, traceback
from collections import defaultdict as ddict

ROUTES = {}
EXTRA_AUTH = ddict(list)
BUCKET = 'caraza-harter-cs301'
ADMIN_EMAIL = 'tylerharter@gmail.com'

s3 = None # client

# decorators
def route(fn):
    ROUTES[fn.__name__] = fn
    return fn

# @admin must be after @route
def admin(fn):
    EXTRA_AUTH[fn.__name__].append(admin_check)
    return fn

def admin_check(user):
    if user['email'] != ADMIN_EMAIL:
        raise Exception('admin required')
    return None

def get_user(event):
    token = event['GoogleToken']
    req = urllib.request.Request('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+token)
    response = urllib.request.urlopen(req)
    status = json.loads(response.read())
    return status

@route
@admin
def put_question(user, event):
    question_id = '%.2f' % time.time()
    question = {'id': question_id, 'question': event['question']}
    for path in ['questions/%s.json'%question_id, 'questions/curr.json']:
        s3.put_object(Bucket=BUCKET,
                      Key=path,
                      Body=bytes(json.dumps(question, indent=2), 'utf-8'),
                      ContentType='text/json',
        )
    return (200, {'message': 'question saved'})

def get_question_raw():
    try:
        response = s3.get_object(Bucket=BUCKET, Key='questions/curr.json')
        txt = response['Body'].read().decode('utf-8')
        return json.loads(txt)
    except Exception as e:
        return None
@route
def get_question(user, event):
    path = 'questions/curr.json'
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')
    return (200, question)

@route
def answer(user, event):  
    user_id = user['sub']
    question_id = event['question_id']
    answer = event['answer']

    # is it current?
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')
    if question_id != question['id']:
        return (500, 'question has changed, please refresh')

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
        return (500, 'answer too long')

@route
@admin
def get_answer_counts(user, event):
    question = get_question_raw()
    if question == None:
        return (500, 'no question set')

    user_id = user['sub']
    path = 'questions/%s/answers' % question['id']
    files = s3.list_objects(Bucket=BUCKET, Prefix=path, MaxKeys=10000)['Contents']

    # count answers/errors
    response = {'errors': ddict(int), 'answers': ddict(int)}
    for obj in files:
        key = obj['Key']
        name = key.split('/')[-1]
        try:
            b = base64.b64decode(name)
            txt = str(b, 'utf-8')
            row = json.loads(txt)
            response['answers'][row['answer']] += 1
        except Exception as e:
            response['errors'][str(e)] += 1
            continue
    return (200, response)

def error(message):
    return {
        "isBase64Encoded": False,
        "statusCode": 500,
        "headers": {},
        "body": message
    }

def save_user_info(user):
    path = 'users/%s.json' % user['sub']
    try:
        boto3.resource('s3').Object(BUCKET, path).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            # does not exist yet
            s3.put_object(Bucket=BUCKET,
                          Key=path,
                          Body=bytes(json.dumps(user, indent=2), 'utf-8'),
                          ContentType='text/json',
            )
        else:
            raise e

def lambda_handler(event, context):
    # cache S3 client
    global s3
    if s3 == None:
        s3 = boto3.client('s3')

    # identify user
    try:
        user = get_user(event)
    except Exception as e:
        return error('exception thrown during authentication')
    if not user['email_verified']:
        return error('google email not verified')
    save_user_info(user)

    # invoke
    fn = ROUTES.get(event['fn'], None)

    if fn == None:
        return error('no route for '+event['fn'])
    try:
        for checker in EXTRA_AUTH[event['fn']]:
            checker(user)
        code, data = fn(user, event)
    except Exception as e:
        return error('Exception: '+str(e) + ' '+traceback.format_exc())

    # result
    return {
        "isBase64Encoded": False,
        "statusCode": code,
        "headers": {},
        "body": data
    }
