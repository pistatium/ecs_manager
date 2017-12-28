# coding: utf-8

from ecs_manager.functions import set_variables, merge_environ


def test_set_variables():
    d = [{
        u'int': 123,
        u'str': u'{{env}}',
        u'dict': {u'nested_str': u'{{ env }}'},
        u'list': [u'{{ env }}', {u'hoge': u'{{ hoge }}'}]
    }, ]
    variables = {u'hoge': u'hogehoge', u'env': u'test'}
    set_variables(d, variables)
    assert d == [{
        u'int': 123,
        u'str': u'test',
        u'dict': {u'nested_str': u'test'},
        u'list': [u'test', {u'hoge': u'hogehoge'}]
    }, ]


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

