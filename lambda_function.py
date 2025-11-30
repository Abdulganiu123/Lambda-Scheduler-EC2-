import os
import json
import logging
import boto3
from botocore.exceptions import ClientError

log = logging.getLogger()
log.setLevel(logging.INFO)

ec2 = boto3.client("ec2")
sns = boto3.client("sns")

# Config (set in Lambda environment variables)
ENV_TAG_KEY = os.getenv("ENV_TAG_KEY", "Environment")
ENV_TAG_VALUE = os.getenv("ENV_TAG_VALUE", "Staging")

EXEMPT_TAG_KEY = os.getenv("EXEMPT_TAG_KEY", "ScheduleExempt")
EXEMPT_TAG_VALUE = os.getenv("EXEMPT_TAG_VALUE", "true")

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")  # optional


def get_tag_value(tags, key):
    """Return tag value for key, or None."""
    if not tags:
        return None
    for t in tags:
        if t.get("Key") == key:
            return t.get("Value")
    return None


def lambda_handler(event, context):
    """
    EventBridge sends: {"action": "start"} or {"action": "stop"}
    """
    action = (event.get("action") or "").lower()
    if action not in ("start", "stop"):
        raise ValueError("event.action must be 'start' or 'stop'")

    state_filter = "stopped" if action == "start" else "running"

    filters = [
        {"Name": f"tag:{ENV_TAG_KEY}", "Values": [ENV_TAG_VALUE]},
        {"Name": "instance-state-name", "Values": [state_filter]},
    ]

    to_change = []
    skipped = []

    try:
        paginator = ec2.get_paginator("describe_instances")
        for page in paginator.paginate(Filters=filters):
            for r in page.get("Reservations", []):
                for inst in r.get("Instances", []):
                    tags = inst.get("Tags", [])
                    exempt_val = get_tag_value(tags, EXEMPT_TAG_KEY)

                    if exempt_val == EXEMPT_TAG_VALUE:
                        skipped.append(inst["InstanceId"])
                    else:
                        to_change.append(inst["InstanceId"])

        if not to_change:
            log.info("No instances to %s. skipped=%s", action, skipped)
            return {"ok": True, "action": action, "changed": [], "skipped": skipped}

        if action == "start":
            ec2.start_instances(InstanceIds=to_change)
        else:
            ec2.stop_instances(InstanceIds=to_change)

        result = {"ok": True, "action": action, "changed": to_change, "skipped": skipped}
        log.info(json.dumps(result))

        if SNS_TOPIC_ARN:
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=json.dumps(result))

        return result

    except ClientError as e:
        log.exception("AWS API error")
        raise
