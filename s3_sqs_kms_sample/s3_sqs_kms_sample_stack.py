from aws_cdk import (
    aws_s3 as s3
    ,aws_sqs as sqs
    ,aws_kms as kms
    ,aws_iam as iam
    ,aws_s3_notifications as aws_s3_notifications
    ,core)

from services.iam_service import IamService


class S3SqsKmsSampleStack(core.Stack):
    __Role = None
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        
        #Create Role
        S3SqsKmsSampleStack.__Role = IamService.create_role(self)

        #get KMS policy Document
        kms_policy_document = IamService.get_kms_policy_documents(self)

        kms_key=kms.Key(self,
                        id='ssl_s3_sqs_kms_key'
                        ,alias = 'sslS3SqsKmsKey'
                        ,description='This is kms key'
                        ,enabled=True
                        ,enable_key_rotation=True
                        ,policy=kms_policy_document)

        

        #This will create the s3 bucket in AWS
        bucket = s3.Bucket(self,"ssl_s3_bucket_raw_kms",bucket_name="ssl-s3-bucket-kms-raw"
                            ,encryption=s3.BucketEncryption.KMS
                            ,encryption_key=kms_key)
        
        #This will create the sqs in AWS
        queue = sqs.Queue(self,"ssl_sqs_event_queue",queue_name="ssl-sqs-kms-event-queue"
                            ,encryption=sqs.QueueEncryption.KMS
                            ,encryption_master_key=kms_key)

        #queue.node.add_dependency(kms_key)
        bucket.node.add_dependency(queue,kms_key)
        # #Create S3 notification object which points to SQS.
        notification = aws_s3_notifications.SqsDestination(queue)
        filter1=s3.NotificationKeyFilter(prefix="home/")
        
        # #Attach notificaton event to S3 bucket.
        
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED,notification,filter1)
