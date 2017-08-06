#!/usr/bin/python
#
# Deploy GDACK
#

import sys
import shutil
import time
import subprocess
import os
import argparse
import boto3


s3Bucket = "gdack"
epoch_time = int(time.time())
zipFile = "gdack-"+str(epoch_time)+".zip"

print("\nSetting up project...\n")

if os.path.exists('./export'):
    shutil.rmtree("./export")

shutil.copytree('./gdack', './export')

install = subprocess.call(["pip3 install -r ./requirements.txt -t ./export"], shell=True)
if install != 0:
    print("Error Installing Eggs")
    sys.exit(1)

print("\nArchiving repository...\n")

subprocess.call(["cd ./export && zip -r ../"+zipFile+" ."], shell=True)

print("\nUploading to S3...\n")
s3 = boto3.client('s3')
key = zipFile
s3.upload_file(zipFile, s3Bucket, key)

shutil.rmtree("./export")
os.remove("./"+zipFile)

print("\nSuccessfully uploaded: "+zipFile+"\n")

print("\nExecuting CloudFormation...\n")

subprocess.call(["python3 ./infrastructure/gdack.py"], shell=True)

cf = boto3.client('cloudformation')

with open('gdack.template', 'r') as fd:
    template = fd.read()

stackname = 'gdack'
key = zipFile
cf.update_stack(
    StackName=stackname,
    Parameters=[
        {
            "ParameterKey": "lambdaKey",
            "ParameterValue": key
        }
    ],
    Capabilities=[
        "CAPABILITY_NAMED_IAM"
    ],
    TemplateBody=template
)

os.remove('./gdack.template')

print("\nCloudFormation Successfully Started for "+env+"...\n")
sys.exit(0)
