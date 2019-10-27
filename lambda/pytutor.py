# Copyright 2018 Tyler Caraza-Harter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json, random, time

from lambda_framework import *

@route
@user
def pytutor_test(user, event):
    path = 'pytutor/dev-test.json'
    count = s3().read_json_default(path, default=1)
    s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(count+1, indent=2), 'utf-8'),
                    ContentType='text/json')
    return (200, "called %d times" % count)
