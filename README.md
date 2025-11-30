# AWS Non-Prod Cost Scheduler (EC2)

A small, practical automation to reduce AWS costs by stopping and starting **non-production EC2 instances** on a schedule.

It uses:
- **EventBridge** (scheduled rules)
- **AWS Lambda (Python / boto3)** to start/stop instances
- **Tag-based targeting** so production resources are not impacted
- Optional **SNS notifications** for visibility

---

## How it works

This Lambda finds EC2 instances that match:
- `Environment=Staging` (configurable)
- Current state:
  - `running` → when stopping
  - `stopped` → when starting

It also supports a safety tag to exclude instances:
- `ScheduleExempt=true` (configurable)

---

## Required Tags

Tag your non-prod instances:

| Tag Key | Tag Value |
|--------|-----------|
| Environment | Staging |

Optional exemption tag:

| Tag Key | Tag Value |
|--------|-----------|
| ScheduleExempt | true |

---

## Lambda Environment Variables

| Variable | Default | Description |
|---------|---------|-------------|
| ENV_TAG_KEY | Environment | Tag key used to identify non-prod instances |
| ENV_TAG_VALUE | Staging | Tag value used to identify non-prod instances |
| EXEMPT_TAG_KEY | ScheduleExempt | Tag key used to exempt instances |
| EXEMPT_TAG_VALUE | true | Tag value used to exempt instances |
| SNS_TOPIC_ARN | (empty) | If set, publishes a summary notification |

---

## EventBridge Schedule Setup

Create two scheduled EventBridge rules:

### 1) Stop non-prod (after hours)
Target input:
```json
{ "action": "stop" }
