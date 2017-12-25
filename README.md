# ECS manager

[![PyPI version](https://badge.fury.io/py/ecs-manager.svg)](https://badge.fury.io/py/ecs-manager)

It is a wrapper tool for using AWS ECS.

You can execute from task registration to service startup with a simple command.

## Usage

```
pip install ecs_manager

ecs_manager deploy_service test-service -c default -t "[{\"name\":\"sleep\",\"image\":\"busybox\",\"cpu\":10,\"command\":[\"sleep\",\"360\"],\"memory\":10,\"essential\":true}]" -s '{"desiredCount": 1}'
```


__NAME__

The name of the service you create

__cluster__

AWS ECS Cluster name

__task_container_definition__

Task Container Definition(JSON).

http://docs.aws.amazon.com/en_us/AmazonECS/latest/developerguide/example_task_definitions.html

for example. 

```
    {
      "name": "wordpress",
      "links": [
        "mysql"
      ],
      "image": "wordpress",
      "essential": true,
      "portMappings": [
        {
          "containerPort": 80,
          "hostPort": 80
        }
      ],
      "memory": 500,
      "cpu": 10
    },
    {
      "environment": [
        {
          "name": "MYSQL_ROOT_PASSWORD",
          "value": "password"
        }
      ],
      "name": "mysql",
      "image": "mysql",
      "cpu": 10,
      "memory": 500,
      "essential": true
    } 
```

__service_definition__

Service definition(JSON).

http://docs.aws.amazon.com/AmazonECS/latest/developerguide/service_definition_parameters.html

for example, 

```
{"desiredCount": 1}
```

`name` will be overrided by NAME, you passed command.


__environment__

You can also override envirnments variables in `containerDefinitions`.

