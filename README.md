# caraza-harter-com
For www.caraza-harter.com and tyler.caraza-harter.com

## Setup

The lambdas depend on a bsoup-base layer.  You can create it like this:

python -m venv bsoup
source ./bsoup/bin/activate
pip install beautifulsoup4
(cd bsoup && zip -r - .) > bsoup-base.zip 
aws lambda publish-layer-version --layer-name bsoup-base --zip-file fileb://bsoup-base.zip 
deactivate
