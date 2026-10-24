import pytest

from configobj import ConfigObj, Section


@pytest.mark.parametrize('nested', [False, True])
@pytest.mark.parametrize('method', ['assign', 'update', 'merge'])
@pytest.mark.parametrize('replacement', ['mapping', 'section', 'scalar'])
def test_replacing_value_keeps_section_order_consistent(nested, method, replacement):
    config = ConfigObj()
    target = config
    if nested:
        config['outer'] = {}
        target = config['outer']
    target['before'] = 'first'
    target['value'] = {'child': 'old'} if replacement == 'scalar' else 'old'
    target['after'] = 'last'
    target.comments['value'] = ['# keep this comment']
    target.inline_comments['value'] = '# inline'
    if replacement == 'scalar':
        value = 'new'
    elif replacement == 'mapping':
        value = {'child': 'new'}
    else:
        value = Section(target, target.depth + 1, config, {'child': 'new'}, name='value')

    if method == 'assign':
        target['value'] = value
    else:
        getattr(target, method)({'value': value})

    assert target.scalars == (['before', 'after', 'value'] if replacement == 'scalar'
                              else ['before', 'after'])
    assert target.sections == ([] if replacement == 'scalar' else ['value'])
    assert target.comments['value'] == ['# keep this comment']
    assert target.inline_comments['value'] == '# inline'
    assert target.keys().count('value') == 1
    assert ConfigObj(config.write()).dict() == config.dict()
    target.pop('value')
    assert target.keys() == ['before', 'after']


def test_same_kind_replacement_keeps_position_and_rejected_value_keeps_section():
    config = ConfigObj({'a': 'one', 'b': 'two', 'c': 'three'}, stringify=False)
    config['b'] = 'new'
    assert config.scalars == ['a', 'b', 'c']
    config['section'] = {'child': 'old'}
    config['other'] = {}
    config['section'] = {'child': 'new'}
    assert config.sections == ['section', 'other']
    with pytest.raises(TypeError):
        config['section'] = 42
    assert config.sections == ['section', 'other']
    assert 'section' not in config.scalars
    assert config['section']['child'] == 'new'


def test_unrepr_dictionary_is_a_scalar_and_can_replace_a_section():
    config = ConfigObj(unrepr=True)
    config['before'] = 'first'
    config['value'] = {'child': 'section'}
    config['after'] = 'last'
    config.__setitem__('value', {'child': 'literal'}, unrepr=True)
    assert config.scalars == ['before', 'after', 'value']
    assert config.sections == []
    assert not isinstance(config['value'], Section)
    assert ConfigObj(config.write(), unrepr=True).dict() == config.dict()


def test_invalid_section_contents_keep_existing_scalar_order():
    config = ConfigObj({'before': 'first', 'value': 'old', 'after': 'last'}, stringify=False)
    with pytest.raises(TypeError):
        config['value'] = {'child': 42}
    assert config.scalars == ['before', 'value', 'after']
    assert config.sections == []
    assert config['value'] == 'old'
