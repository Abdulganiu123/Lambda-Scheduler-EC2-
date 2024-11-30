This repository contains an AWS Lambda function that is triggered by an EventBridge Scheduler to stop EC2 instances in a lower environment based on specific tags. The function is designed to operate during non-business hours and on weekends, ensuring efficient resource management and cost savings. Additionally, an Amazon SNS topic is integrated to provide notifications whenever the Lambda function is triggered by the EventBridge scheduler.

Features
EventBridge Scheduler: Automates the triggering of the Lambda function based on a cron schedule.
EC2 Instance Management: Stops EC2 instances in a lower environment based on user-defined tags.
SNS Notifications: Sends notifications to a specific SNS topic whenever the Lambda function is executed by the scheduler.
Cost Efficiency: Helps reduce costs by stopping non-essential instances during off-hours.
Architecture
The architecture consists of the following components:

AWS Lambda Functions: Executes the logic to stop EC2 instances.
Amazon EventBridge: Handles the scheduling and triggering of the Lambda function.
Amazon SNS: Sends notifications to subscribed endpoints when the function runs.
