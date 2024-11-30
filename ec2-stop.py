import boto3
import json

def lambda_handler(event, context):
    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    # Define the filtering criteria for the instances you want to stop
    filters = [
        {
            'Name': 'tag:Environment',
            'Values': ['test']  # Change 'test' to your desired tag value
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]

    # Describe instances based on the filter
    response = ec2_client.describe_instances(Filters=filters)

    # List to hold instance IDs that will be stopped
    instances_to_stop = []

    # Loop through instances in the response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])

    # Stop instances if there are any
    if instances_to_stop:
        ec2_client.stop_instances(InstanceIds=instances_to_stop)
        print(f'Stopped instances: {instances_to_stop}')
    else:
        print('No running instances found to stop.')