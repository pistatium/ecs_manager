# ECS manager

[![PyPI version](https://badge.fury.io/py/ecs-manager.svg)](https://badge.fury.io/py/ecs-manager)

AWS ECSのラッパーコマンドです.

環境変数などを組み合わせたECSのタスクをシンプルなコマンドでデプロイできます。

## 使い方

前提条件として AWS CLI が使えるよう環境変数がセットされている必要があります。

```
pip3 install ecs_manager

# Example
ecs_manager deploy-service test-service -c default -t "[{\"name\":\"sleep\",\"image\":\"busybox\",\"cpu\":10,\"command\":[\"sleep\",\"360\"],\"memory\":10,\"essential\":true}]" -s '{"desiredCount": 1}'

# => ECS 上にサービスが生成されます
```


__NAME__
作ろうとしているECSのサービス名です。

__cluster__

ECSのクラスタ名

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

__variables__

if you set variables on your task, use `{{ xxx }}` in task.json with option `-v {'xxx': 'value'}`


### task definition only mode
You can add `--task_definition_only` option for registering task definition without updating ecs service
```
ecs_manager deploy-service test-service --task_definition_only -c default -t "[{\"name\":\"sleep\",\"image\":\"busybox\",\"cpu\":10,\"command\":[\"sleep\",\"360\"],\"memory\":10,\"essential\":true}]" -s '{"desiredCount": 1}'
```
