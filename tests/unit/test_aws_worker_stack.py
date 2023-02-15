import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_worker.aws_worker_stack import AwsWorkerStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_worker/aws_worker_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsWorkerStack(app, "aws-worker")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
