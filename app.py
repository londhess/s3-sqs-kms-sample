#!/usr/bin/env python3

from aws_cdk import core

from s3_sqs_kms_sample.s3_sqs_kms_sample_stack import S3SqsKmsSampleStack


app = core.App()

S3SqsKmsSampleStack(app, "s3-sqs-kms-sample",env={'region': 'ap-south-1'})

app.synth()
