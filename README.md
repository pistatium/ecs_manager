# ECS manager

[![PyPI version](https://badge.fury.io/py/ecs-manager.svg)](https://badge.fury.io/py/ecs-manager)

Easy deploy to aws ecs cluster.

## Usage

```
pip install ecs_manager
ecs_manager deploy_service test-service -c default -t "[{\"name\":\"sleep\",\"image\":\"busybox\",\"cpu\":10,\"command\":[\"sleep\",\"360\"],\"memory\":10,\"essential\":true}]" -s '{"desiredCount": 1}'
```

