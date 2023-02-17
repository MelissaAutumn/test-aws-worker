#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_worker.thunderbird_website.preview_stack import PreviewStack

preview_env_id = os.getenv('PS_PREVIEW_ENV_ID', 'fake-branch-name-400')  # Formatted like: `{Branch Name}-{PR Number}`

app = cdk.App()
PreviewStack(app, f"PreviewEnvironment-{preview_env_id}",
    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    env=cdk.Environment(account=os.getenv('PS_AWS_ACCOUNT_ID'), region=os.getenv('PS_AWS_REGION', 'us-west-1')),
)

app.synth()
