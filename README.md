# ECS SERVICE manager

Easy deploy to aws ecs cluster.

## Usage

```
pip install ecs_service_manager
ecs_service_manager deploy_service test-service -c default -t "[{\"name\":\"sleep\",\"image\":\"busybox\",\"cpu\":10,\"command\":[\"sleep\",\"360\"],\"memory\":10,\"essential\":true}]" -s '{"desiredCount": 1}'
```

