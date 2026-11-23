import pytest

from configobj import ConfigObj, SimpleVal, flatten_errors
from configobj.validate import Validator, VdtTypeError, VdtValueError


SPEC = ['[devices]', '[[__many__]]', '__name__ = integer(100,10000000)',
        'label = string', 'count = integer(default=3)']


@pytest.mark.parametrize('name', ['100', '10000000', '00100'])
def test_integer_names_are_checked_without_renaming(name):
    config = ConfigObj({'devices': {name: {'label': 'meter'}}}, configspec=SPEC)
    assert config.validate(Validator(), validate_section_names=True) is True
    assert config['devices'].sections == [name]
    assert config['devices'][name].name == name
    assert config['devices'][name]['count'] == 3
    assert '__name__' not in config['devices'][name]
    assert '__name__' not in config['devices'][name].default_values


@pytest.mark.parametrize('name', ['99', '10000001', 'invalid'])
def test_invalid_names_report_section_path(name):
    config = ConfigObj({'devices': {name: {'label': 'meter'}}}, configspec=SPEC)
    result = config.validate(Validator(), preserve_errors=True, validate_section_names=True)
    errors = flatten_errors(config, result)
    assert len(errors) == 1
    assert errors[0][:2] == (['devices', name], '__name__')
    assert isinstance(errors[0][2], (VdtTypeError, VdtValueError))
    assert config['devices'][name]['count'] == 3


def test_name_and_field_errors_are_both_preserved():
    config = ConfigObj({'devices': {'bad': {'label': 'meter', 'count': 'bad'}}}, configspec=SPEC)
    result = config.validate(Validator(), preserve_errors=True, validate_section_names=True)
    errors = flatten_errors(config, result)
    assert {tuple(path + [key]) for path, key, error in errors} == {
        ('devices', 'bad', '__name__'), ('devices', 'bad', 'count')}
    assert all(isinstance(error, VdtTypeError) for _, _, error in errors)


def test_default_mode_preserves_real_name_fields():
    config = ConfigObj({'group': {'__name__': '42'}}, configspec=['[group]', '__name__ = integer'])
    assert config.validate(Validator()) is True
    assert config['group']['__name__'] == 42


def test_opt_in_reserves_schema_key_without_mutating_data_field():
    config = ConfigObj({'123': {'__name__': 'ordinary data'}},
                       configspec=['[__many__]', '__name__ = integer'])
    assert config.validate(Validator(), validate_section_names=True) is True
    assert config['123']['__name__'] == 'ordinary data'


def test_copy_mode_does_not_create_name_value_or_comments():
    config = ConfigObj({'devices': {'123': {'label': 'meter'}}}, configspec=SPEC)
    assert config.validate(Validator(), copy=True, validate_section_names=True) is True
    child = config['devices']['123']
    assert child['count'] == 3
    assert '__name__' not in child.comments
    assert all('__name__' not in line for line in config.write())


def test_explicit_named_section_and_nested_repeated_sections():
    spec = ['[devices]', '__name__ = option(devices)', '[[__many__]]',
            '__name__ = integer', '[[[__many__]]]', '__name__ = string(min=2)']
    config = ConfigObj({'devices': {'123': {'ok': {}, 'x': {}}}}, configspec=spec)
    errors = flatten_errors(config, config.validate(
        Validator(), preserve_errors=True, validate_section_names=True))
    assert errors[0][:2] == (['devices', '123', 'x'], '__name__')
    assert len(errors) == 1


def test_boolean_error_mode():
    config = ConfigObj({'bad': {}, '123': {}}, configspec=['[__many__]', '__name__ = integer'])
    assert config.validate(Validator(), validate_section_names=True) == {'bad': False, '123': True}


def test_custom_validator_receives_original_name():
    names = []

    def check_name(value):
        names.append(value)
        if not value.startswith('device-'):
            raise VdtValueError(value)
        return value.upper()

    config = ConfigObj({'device-\u96ea': {}}, configspec=['[__many__]', '__name__ = device'])
    validator = Validator({'device': check_name})
    assert config.validate(validator, validate_section_names=True) is True
    assert names == ['device-\u96ea']
    assert config.sections == ['device-\u96ea']


def test_root_name_check_is_rejected_only_when_enabled():
    config = ConfigObj({'__name__': '42'}, configspec=['__name__ = integer'])
    with pytest.raises(ValueError, match='config root'):
        config.validate(Validator(), validate_section_names=True)
    assert config.validate(Validator()) is True


def test_missing_default_section_is_not_satisfied_by_its_name():
    config = ConfigObj([], configspec=['[required]', '__name__ = string', 'value = integer'])
    assert config.validate(Validator(), validate_section_names=True) is False


def test_simple_validator_and_repeated_validation():
    config = ConfigObj({'123': {}}, configspec=['[__many__]', '__name__ = integer'])
    assert config.validate(SimpleVal(), validate_section_names=True) is True
    assert config.validate(Validator(), validate_section_names=True) is True
    assert config.validate(Validator(), validate_section_names=True) is True
    assert config['123'].scalars == []
