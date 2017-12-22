# coding: utf-8

import json

import click
import boto3

from ecs_manager.utils.json_util import json_dumps


client = boto3.client('ecs')


def json_validator(context, param, value):
    if not value:
        raise click.BadParameter('{} definition is required'.format(param.name))
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
def deploy_service(name, cluster, task_container_definition, service_definition):
    status = check_task_status(name, task_container_definition)
    
    if status['changed']:
        click.echo(status)
        res = client.register_task_definition(family=name, containerDefinitions=task_container_definition)
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



def check_task_status(name, container_definition):
    saved_task = client.list_task_definitions(familyPrefix=name, sort='DESC')
    if not saved_task['taskDefinitionArns']:
        return {'changed': True, 'arn': None}
    latest_task_arn = saved_task['taskDefinitionArns'][0]
    saved_definition = client.describe_task_definition(taskDefinition=latest_task_arn)['taskDefinition']['containerDefinitions']
    changed = regularization_task(saved_definition) != regularization_task(container_definition)
    return {'changed': changed, 'arn': latest_task_arn}


def regularization_task(task):
    result = []
    for container in task:
        result.append({k: v for k, v in container.items() if v != []})
    return result


def main():
    cmd()


if __name__ == '__main__':
    main()
