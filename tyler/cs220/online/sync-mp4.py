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

import boto3, uuid, os, io, json, mimetypes, git, sys

# https://s3.us-east-2.amazonaws.com/caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0/index.html
#
# to invalidate SDN, do this:
# aws cloudfront create-invalidation --distribution-id E2MK8CNX2PPPIY --paths "/*"

def main():
    s3 = boto3.client('s3')
    bucket = "caraza-harter-4dcf7c05-8564-11e8-a86d-6a00020017a0" #self.get_web_bucket('%s.caraza-harter.com' % self.subdomain)

    for root, _, names in os.walk("lec"):
        for name in names:
            if not name.endswith(".mp4"):
                continue
            path = os.path.join(root, name)
            s3_path = f"cs220/online/{path}"
            with open(path, "rb") as f:
                if len(sys.argv) > 1:
                    for v in sys.argv[1:]:
                        if v in s3_path:
                            break
                    else:
                        continue
                print(s3_path)
                s3.put_object(Bucket=bucket, Key=s3_path, Body=f)

if __name__ == '__main__':
    main()
