import boto3
import json

def lambda_handler(event, context):
    # Create an EC2 client
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    # Define the filtering criteria for the instances you want to start
    filters = [
        {
            'Name': 'tag:Environment',
            'Values': ['Staging']  # Change 'test' to your desired tag value
        },
        {
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }
    ]

    # Describe instances based on the filter
    response = ec2_client.describe_instances(Filters=filters)

    # List to hold instance IDs that will be started
    instances_to_start = []

    # Loop through instances in the response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_start.append(instance['InstanceId'])

    # Start instances if there are any
    if instances_to_start:
        ec2_client.start_instances(InstanceIds=instances_to_start)
        print(f'Started instances: {instances_to_start}')

        # Send a success message to SNS
        sns_topic_arn = 'arn:aws:sns:us-east-1:329551316753:instancestopped'  # Replace with your SNS topic ARN
        sns_message = f'Successfully started the following instances: {instances_to_start}'
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=sns_message
        )
        print('Success message sent to SNS.')
    else:
        print('No stopped instances found to start.')