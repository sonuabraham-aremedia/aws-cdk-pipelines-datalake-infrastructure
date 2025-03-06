# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import re

# Environments (targeted at accounts)
DEPLOYMENT = 'Deployment'
DEV = 'Dev'
TEST = 'Test'
PROD = 'Prod'

# The following constants are used to map to parameter/secret paths
ENVIRONMENT = 'environment'
GITHUB_REPOSITORY_OWNER_NAME = 'sonuabraham-aremedia'
GITHUB_REPOSITORY_NAME = 'aws-cdk-pipelines-datalake-infrastructure'
ACCOUNT_ID = '391970746680'
REGION = 'ap-southeast-2'
VPC_CIDR = '10.0.0.0/16'

# Manual Inputs
LOGICAL_ID_PREFIX = 'data'
RESOURCE_NAME_PREFIX = 'dl'

# Secrets Manager Inputs
GITHUB_TOKEN = 'github-personal-access-token'

# Used in Automated Outputs
VPC_ID = 'vpc-06b64296a01d51a20'
AVAILABILITY_ZONE_1 = 'ap-southeast-2a'
AVAILABILITY_ZONE_2 = 'ap-southeast-2b'
AVAILABILITY_ZONE_3 = 'ap-southeast-2c'
SUBNET_ID_1 = 'subnet-0864ac1b6479f0850'
SUBNET_ID_2 = 'subnet-01b13de8cc975d87e'
SUBNET_ID_3 = 'subnet-0b6237c102e0fde63'
ROUTE_TABLE_1 = 'rtb-0f3a4dff5b170a396'
ROUTE_TABLE_2 = 'rtb-0cd1ff7ebedc127ad'
ROUTE_TABLE_3 = 'rtb-05bae96d06af12e48'
SHARED_SECURITY_GROUP_ID = 'sg-0e23f2a97722d13a3'
S3_KMS_KEY = '9de1dc97-7f01-41df-b6be-72e7834954aa'
S3_ACCESS_LOG_BUCKET = 'datalake-log-bucket-123456789'
S3_RAW_BUCKET = 'datalake-raw-bucket-123456789'
S3_CONFORMED_BUCKET = 'datalake-confirmed-bucket-123456789'
S3_PURPOSE_BUILT_BUCKET = 'datalake-purpose-bucket-123456789'


def get_local_configuration(environment: str) -> dict:
    """
    Provides manually configured variables that are validated for quality and safety.

    @param: environment str: The environment used to retrieve corresponding configuration
    @raises: Exception: Throws an exception if the resource_name_prefix does not conform
    @raises: Exception: Throws an exception if the requested environment does not exist
    @returns: dict:
    """
    local_mapping = {
        DEPLOYMENT: {
            ACCOUNT_ID: '391970746680',
            REGION: 'ap-southeast-2',
            GITHUB_REPOSITORY_OWNER_NAME: 'sonubraham-aremedia',
            # If you use GitHub / GitHub Enterprise, this will be the organization name
            GITHUB_REPOSITORY_NAME: 'aws-cdk-pipelines-datalake-infrastructure',
            # Use your forked repo here!
            # This is used in the Logical Id of CloudFormation resources
            # We recommend capital case for consistency. e.g. DataLakeCdkBlog
            LOGICAL_ID_PREFIX: 'DataLakeCdkBlog',
            # This is used in resources that must be globally unique!
            # It may only contain alphanumeric characters, hyphens, and cannot contain trailing hyphens
            # E.g. unique-identifier-data-lake
            RESOURCE_NAME_PREFIX: 'dl',
        },
        DEV: {
            ACCOUNT_ID: '391970746680',
            REGION: 'ap-southeast-2',
            VPC_CIDR: '10.0.0.0/16'
        },
        TEST: {
            ACCOUNT_ID: '391970746680',
            REGION: 'ap-southeast-2',
            VPC_CIDR: '10.0.0.0/16'
        },
        PROD: {
            ACCOUNT_ID: '391970746680',
            REGION: 'ap-southeast-2',
            VPC_CIDR: '10.0.0.0/16'
        }
    }

    resource_prefix = local_mapping[DEPLOYMENT][RESOURCE_NAME_PREFIX]
    if (
        not re.fullmatch('^[a-z|0-9|-]+', resource_prefix)
        or '-' in resource_prefix[-1:] or '-' in resource_prefix[1]
    ):
        raise Exception('Resource names may only contain lowercase Alphanumeric and hyphens '
                        'and cannot contain leading or trailing hyphens')

    if environment not in local_mapping:
        raise Exception(f'The requested environment: {environment} does not exist in local mappings')

    return local_mapping[environment]


def get_environment_configuration(environment: str) -> dict:
    """
    Provides all configuration values for the given target environment

    @param environment str: The environment used to retrieve corresponding configuration

    @return: dict:
    """
    cloudformation_output_mapping = {
        ENVIRONMENT: environment,
        VPC_ID: f'{environment}VpcId',
        AVAILABILITY_ZONE_1: f'{environment}AvailabilityZone1',
        AVAILABILITY_ZONE_2: f'{environment}AvailabilityZone2',
        AVAILABILITY_ZONE_3: f'{environment}AvailabilityZone3',
        SUBNET_ID_1: f'{environment}SubnetId1',
        SUBNET_ID_2: f'{environment}SubnetId2',
        SUBNET_ID_3: f'{environment}SubnetId3',
        ROUTE_TABLE_1: f'{environment}RouteTable1',
        ROUTE_TABLE_2: f'{environment}RouteTable2',
        ROUTE_TABLE_3: f'{environment}RouteTable3',
        SHARED_SECURITY_GROUP_ID: f'{environment}SharedSecurityGroupId',
        S3_KMS_KEY: f'{environment}S3KmsKeyArn',
        S3_ACCESS_LOG_BUCKET: f'{environment}S3AccessLogBucket',
        S3_RAW_BUCKET: f'{environment}RawBucketName',
        S3_CONFORMED_BUCKET: f'{environment}ConformedBucketName',
        S3_PURPOSE_BUILT_BUCKET: f'{environment}PurposeBuiltBucketName',
    }

    return {**cloudformation_output_mapping, **get_local_configuration(environment)}


def get_all_configurations() -> dict:
    """
    Returns a dict mapping of configurations for all environments.
    These keys correspond to static values, CloudFormation outputs, and Secrets Manager (passwords only) records.

    @return: dict:
    """
    return {
        DEPLOYMENT: {
            ENVIRONMENT: DEPLOYMENT,
            GITHUB_TOKEN: '/DataLake/GitHubToken',
            **get_local_configuration(DEPLOYMENT),
        },
        DEV: get_environment_configuration(DEV),
        TEST: get_environment_configuration(TEST),
        PROD: get_environment_configuration(PROD),
    }


def get_logical_id_prefix() -> str:
    """Returns the logical id prefix to apply to all CloudFormation resources

    @return: str:
    """
    return get_local_configuration(DEPLOYMENT)[LOGICAL_ID_PREFIX]


def get_resource_name_prefix() -> str:
    """Returns the resource name prefix to apply to all resources names

    @return: str:
    """
    return get_local_configuration(DEPLOYMENT)[RESOURCE_NAME_PREFIX]
