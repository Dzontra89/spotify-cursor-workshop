# Spotify Workshop Project

This project is a part of the Spotify Workshop, which includes various AWS services such as S3, SQS, and Lambda.

## Table of Contents
- [Data](#data)
- [Backend (BE)](#backend-be)
- [Frontend (FE)](#frontend-fe)

## Data

### Spotify Ingestion Lambda Function

The Lambda function in this project processes messages from an SQS queue and interacts with S3 buckets. The function's timeout is set to the maximum allowed value of 15 minutes.

### How to Generate and Deploy the Current Stack and Resources

1. **Install the AWS CDK**: Ensure you have the AWS CDK installed globally on your machine.
    ```sh
    npm install -g aws-cdk
    ```

2. **Bootstrap Your Environment**: Before deploying any AWS CDK stacks, you need to bootstrap your environment.
    ```sh
    cdk bootstrap
    ```

3. **Deploy the Stack**: Deploy the stack to your AWS account.
    ```sh
    cdk deploy
    ```

4. **Synthesize the CloudFormation Template**: If you want to generate the CloudFormation template without deploying, run:
    ```sh
    cdk synth
    ```

## Backend (BE)
*To be populated later.*

## Frontend (FE)
*To be populated later.*
