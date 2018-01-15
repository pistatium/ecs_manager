# coding: utf-8

import re
from builtins import str as text

def set_variables(definition, variables):
    def traverse(obj):
        if isinstance(obj, (str, text)):
            for k, v in variables.items():
                obj = re.sub(u'{{\s?' + k + u'\s?}}', v, obj)
            return obj
        if isinstance(obj, dict):
            for key, value in obj.items():
                obj[key] = traverse(value)
        if isinstance(obj, list):
            obj = [traverse(o) for o in obj]
        return obj
    traverse(definition)
    return definition


def merge_environ(container_definition, env_override):
    for cd in container_definition:
        env = {}
        for e in cd.get('environment', []):
            env[e['name']] = e['value']
        for key, val in env_override.items():
            env[key] = val
        cd['environment'] = [{'name': key, 'value': env[key]} for key in sorted(env.keys())]


def check_task_status(client, name, container_definition):
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


