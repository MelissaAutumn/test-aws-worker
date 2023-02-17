import os
from pathlib import Path

import aws_cdk
from aws_cdk import (
    Duration,
    Stack,
    aws_s3 as s3,
    aws_s3_deployment as s3_deployment,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as cloudfront_origins,
    # aws_sqs as sqs,
)
from constructs import Construct

class PreviewStackS3(Stack):
    """Preview stack hosted on Amazon S3, and fronted by Cloudfront. Note: I'm not sure if this fully works it was used in testing."""
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        bucket = s3.Bucket(self, id="Bucket", auto_delete_objects=True, removal_policy=aws_cdk.RemovalPolicy.DESTROY)
        distribution = cloudfront.Distribution(self, id="Distribution", default_behavior={
            'origin': cloudfront_origins.S3Origin(bucket),
            'viewer_protocol_policy': cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
        })

        aws_cdk.CfnOutput(self,
                          id="DeploymentUrl",
                          value=f"https://{distribution.distribution_domain_name}"
                          )

        s3_deployment.BucketDeployment(self,
                                       id="BucketDeployment",
                                       destination_bucket=bucket,
                                       distribution=distribution,
                                       #distribution_paths=["/", "/index.html"],
                                       memory_limit=256,
                                       sources=[s3_deployment.Source.asset('../thunderbird-website/thunderbird.net/')]
                                       )


