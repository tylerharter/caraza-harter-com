import base64, boto3, botocore, logging, os, sys, json, subprocess, shutil
from flask import Flask

ACCESS_PATH = "projects/{project}/users/{googleId}/curr.json"
CODE_DIR = "./submission"
TEST_DIR = "/tmp/test"

SUBMISSIONS = 'submissions'
BUCKET = 'caraza-harter-cs301'
session = boto3.Session(profile_name='cs301ta')
s3 = session.client('s3')

app = Flask(__name__)

logging.basicConfig(
    handlers=[
        logging.FileHandler("testServer.log"),
        logging.StreamHandler()
    ],
    level=logging.WARNING)

def downloadSubmission(projectPath):
    # a project path will look something like this:
    # projects/p0/users/115799594197844895033/curr.json

    userId = projectPath.split('/')[-2]

    # create user dir for download
    logging.info('download to {}'.format(CODE_DIR))
    if os.path.exists(CODE_DIR):
        shutil.rmtree(CODE_DIR)
    os.mkdir(CODE_DIR)

    # download
    response = s3.get_object(Bucket=BUCKET, Key=projectPath)
    submission = json.loads(response['Body'].read().decode('utf-8'))
    fileContents = base64.b64decode(submission.pop('payload'))
    with open(os.path.join(CODE_DIR, submission['filename']), 'wb') as f:
        f.write(fileContents)
    with open(os.path.join(CODE_DIR, 'meta.json'), 'w') as f:
        f.write(json.dumps(submission, indent=2))

def uploadResult(project, studentID):
    with open("{}/result.json".format(TEST_DIR), "r") as fr:
        serializedResult = fr.read()
    s3.put_object(
        Bucket=BUCKET,
        Key='ta/grading/{}/{}.json'.format(project, studentID),
        Body=serializedResult.encode('utf-8'),
        ContentType='text/plain')

def lookupGoogleId(netId):
    path = 'users/net_id_to_google/%s.txt' % netId
    try:
        response = s3.get_object(Bucket=BUCKET, Key=path)
        net_id = response['Body'].read().decode('utf-8')
        return net_id
    except botocore.exceptions.ClientError as e:
        if not e.response['Error']['Code'] == "NoSuchKey":
            # unexpected error
            logging.warning(
                'Unexpected error when look up Googlg ID:' + e.response['Error']['Code'])
        raise e

def fetchFromS3(project, netId):
    googleId = lookupGoogleId(netId)
    if not googleId:
        return None
    curPath = ACCESS_PATH.format(project=project, googleId=googleId)
    downloadSubmission(curPath)

def sendToDocker(project, netId):
    # create directory to mount inside a docker container
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    shutil.copytree(CODE_DIR, TEST_DIR)
    shutil.copytree("./io", TEST_DIR + "/io")
    # we can't use shutil.copytree here again because TEST_DIR exists
    testCodePath = "./test/{}".format(project)
    for item in os.listdir(testCodePath):
        src = os.path.join(testCodePath, item)
        dest = os.path.join(TEST_DIR, item)
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)

    # run tests inside a docker container
    image = 'python:3.7-stretch' # TODO: find/build some anaconda image

    cmd = ['docker', 'run',                           # start a container
           '-v', os.path.abspath(TEST_DIR)+':/code',  # share the test dir inside
           '-w', '/code',                             # working dir is w/ code
           image,                                     # what docker image?
           'python3', 'testMain.py',
           '-p', project,
           '-i', netId]                      # command to run inside
    logging.info("docker cmd:" + ' '.join(cmd))
    output = subprocess.check_output(cmd)

@app.route('/')
def index():
    return "index"

@app.route('/json/<project>/<netId>')
def gradingJson(project, netId):
    try:
        fetchFromS3(project, netId)
        sendToDocker(project, netId)
        uploadResult(project, netId)
        return json.dumps({})
    except Exception as e:
        logging.warning("Unexpected Error: " + str(e))
        return json.dumps({"error": str(e)})
