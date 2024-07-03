#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_lambda_event_sources as lambda_events,
    aws_s3_notifications as s3n,
    aws_iam as iam,
    aws_ec2 as ec2,
)
from constructs import Construct

class SpotifyWorkshopStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # Internal S3 bucket
        internal_bucket = s3.Bucket(self, "InternalBucket")

        # Output S3 bucket
        output_bucket = s3.Bucket(self, "OutputBucket", public_read_access=True)

        # SQS queue
        queue = sqs.Queue(self, "MyQueue")

        # Lambda function to process SQS messages
        lambda_fn = lambda_.Function(
            self, "MyLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "OUTPUT_BUCKET": output_bucket.bucket_name
            },
            vpc=vpc
        )

        # Grant Lambda permissions
        queue.grant_consume_messages(lambda_fn)
        output_bucket.grant_write(lambda_fn)
        internal_bucket.grant_read(lambda_fn)

        # Add SQS event source to Lambda
        lambda_fn.add_event_source(lambda_events.SqsEventSource(queue))

        # Add S3 notification to SQS
        internal_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SqsDestination(queue)
        )

app = cdk.App()
SpotifyWorkshopStack(app, "SpotifyWorkshopStack")
app.synth()
