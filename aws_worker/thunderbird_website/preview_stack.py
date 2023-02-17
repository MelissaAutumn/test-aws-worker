import os

import aws_cdk
from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets
)
from constructs import Construct


class PreviewStack(Stack):
    """Preview Environments via FarGate Spot"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        site_id = os.getenv('PS_SITE_NAME', 'thunderbird-website')
        namespace = os.getenv('PS_NAMESPACE', 'thunderbird.local')
        docker_directory = os.getenv('PS_DOCKER_DIRECTORY', '../thunderbird-website')
        docker_file = os.getenv('PS_DOCKER_FILE', 'deploy.docker')

        vpc_id = f"{site_id}-vpc"
        asset_id = f"{site_id}-asset"
        task_id = f"{site_id}-task"
        container_id = f"{site_id}-container"
        service_id = f"{site_id}-service"
        cluster_id = f"{site_id}-cluster"

        # New VPC
        vpc = ec2.Vpc(self, id=vpc_id, max_azs=1)

        cluster = ecs.Cluster(self, id=cluster_id, vpc=vpc, enable_fargate_capacity_providers=True)

        cluster.add_default_cloud_map_namespace(name=namespace)

        asset = ecr_assets.DockerImageAsset(self, id=asset_id, directory=docker_directory, file=docker_file)
        # Refer to: https://docs.aws.amazon.com/AmazonECS/latest/userguide/fargate-task-defs.html
        task = ecs.FargateTaskDefinition(self, id=task_id, cpu=256, memory_limit_mib=512)
        container = task.add_container(
            id=container_id,
            image=ecs.ContainerImage.from_docker_image_asset(asset),
            essential=True,
            # Environment Variables for the container
            # environment={},
        )
        container.add_port_mappings(ecs.PortMapping(container_port=80, host_port=80))

        service = ecs_patterns.NetworkLoadBalancedFargateService(self,
                                                                 id=service_id,
                                                                 service_name=site_id,
                                                                 cluster=cluster,
                                                                 cloud_map_options=ecs.CloudMapOptions(name=namespace),
                                                                 task_definition=task,
                                                                 listener_port=80,
                                                                 public_load_balancer=True,
                                                                 capacity_provider_strategies=[
                                                                     ecs.CapacityProviderStrategy(capacity_provider="FARGATE_SPOT", weight=1)
                                                                 ])

        service.service.connections.allow_from_any_ipv4(
            ec2.Port.tcp(80), "http inbound"
        )
