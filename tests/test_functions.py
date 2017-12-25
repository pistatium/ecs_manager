# coding: utf-8

from ecs_manager.functions import merge_environ


def test_merge_environ():
    definition = [
        {
            'environment': [
                {'name': 'hoge', 'value': 'hoge'},
                {'name': 'fuga', 'value': 'fuga'},
            ]
        }, {
        }
    ]

    merge_environ(definition, {'hoge': 'hogehoge', 'piyo': 'piyopiyo'})

    assert definition[0]['environment'][0] == {'name': 'fuga', 'value': 'fuga'}
    assert definition[0]['environment'][1] == {'name': 'hoge', 'value': 'hogehoge'}
    assert definition[0]['environment'][2] == {'name': 'piyo', 'value': 'piyopiyo'}
    assert definition[1]['environment'][0] == {'name': 'hoge', 'value': 'hogehoge'}
    assert definition[1]['environment'][1] == {'name': 'piyo', 'value': 'piyopiyo'}

