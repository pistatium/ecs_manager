# coding: utf-8

import json

import click
import boto3


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
@click.argument('family', help='ecs task name')
@click.option('--cluster', '-c', required=True, help='ecs cluster')
@click.option('--service_definition', '-s', callback=json_validator)
@click.option('--task_definition', '-t', callback=json_validator)
def deploy(family, cluster, service_definition, task_definition):
    ...    
    #print(client.list_services(cluster='monaca-local'))


def main():
    cmd()


if __name__ == '__main__':
    main()
