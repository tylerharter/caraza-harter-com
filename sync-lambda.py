#!/usr/bin/env python3

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

import boto3, zipfile, os, sys

session = boto3.Session(profile_name='default', region_name='us-east-2')
client = session.client('lambda')

def main():
    fname = 'cs301-test'
    if len(sys.argv) == 2:
        if sys.argv[1] == 'prod':
            fname = 'cs301'
        elif sys.argv[1] == 'pytutor':
            fname = 'cs301-pytutor'
    print(client.get_function(FunctionName=fname))

    tmp = 'tmp.zip'
    lambda_dirs = ['lambda']
    for lambda_dir in lambda_dirs:
        with zipfile.ZipFile(tmp, 'w') as z:
            for name in (n for n in os.listdir(lambda_dir) if n.split('.')[-1] in ('py', 'txt')):
                z.write(os.path.join(lambda_dir, name), '/'+name)

    with open(tmp, 'rb') as f:
        response = client.update_function_code(FunctionName=fname, ZipFile=f.read())

    os.remove(tmp)

if __name__ == '__main__':
    main()
