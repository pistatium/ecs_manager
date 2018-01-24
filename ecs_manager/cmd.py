# coding: utf-8

import json
import os.path
import sys

import click
import boto3
from botocore.exceptions import ClientError

from ecs_manager.utils.json_util import json_dumps
from ecs_manager.functions import set_variables, merge_environ, check_task_status

client = boto3.client('ecs')


def json_validator(context, param, value):
    if value is None:
        raise click.BadParameter('{} definition is required'.format(param.name))
    if value.startswith('@'):
        path = value[1:]
        if not os.path.isfile(path):
            raise click.BadParameter('{}: File path `{}` is not found'.format(param.name, path))
        with open(path, 'r') as f:
            value = f.read()
    try:
        return json.loads(value)
    except json.decoder.JSONDecodeError:
        raise click.BadParameter('{} definition is invalid json format'.format(param.name))


@click.group()
def cmd():
    pass


@cmd.command()
@click.argument('name')
@click.option('--cluster', '-c', required=True)
@click.option('--task_container_definition', '-t', callback=json_validator)
@click.option('--service_definition', '-s', callback=json_validator)
@click.option('--environment', '-e', callback=json_validator, default='{}')
@click.option('--variables', '-v', callback=json_validator, default='{}')
def deploy_service(name, cluster, task_container_definition, service_definition, environment, variables):
    variables.update({
        'name': name,
        'cluster': cluster,
    })
    merge_environ(task_container_definition, environment)
    set_variables(task_container_definition, variables)
    set_variables(service_definition, variables)

    status = check_task_status(client, name, task_container_definition)
    
    if status['changed']:
        click.echo(status)
        try:
            res = client.register_task_definition(family=name, containerDefinitions=task_container_definition)
        except ClientError:
            click.echo(repr(sys.exc_info()[1]))
            click.echo(task_container_definition)
            return
        task_arn = res['taskDefinition']['taskDefinitionArn']
        click.echo(task_arn)
    else:
        click.echo('Task definition is not changed')
        task_arn = status['arn']

    res = client.describe_services(cluster=cluster, services=[name, ])
    if not res['services']:
        res = client.create_service(cluster=cluster, serviceName=name, taskDefinition=task_arn, **service_definition)
        click.echo('Created service')
        click.echo(json_dumps(res))
        return
    res = client.update_service(cluster=cluster, service=name, taskDefinition=task_arn, **service_definition)
    click.echo('Updated service')
    click.echo(json_dumps(res))


def main():
    cmd()


if __name__ == '__main__':
    main()
