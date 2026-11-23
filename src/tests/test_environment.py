import io

import pytest

from configobj import ConfigObj, Section, flatten_errors
from configobj.validate import Validator, VdtTypeError


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch):
    # Use a case-sensitive mapping on every OS, including Windows.
    monkeypatch.setattr('os.environ', {})


def test_disabled_by_default(monkeypatch):
    monkeypatch.setenv('PORT', '9000')
    assert ConfigObj({'port': '8000'})['port'] == '8000'


def test_overrides_nested_scalars_without_replacing_sections(monkeypatch):
    monkeypatch.setenv('SERVER', 'not a section')
    monkeypatch.setenv('SERVER__HTTP__PORT', '9000')
    config = ConfigObj({'server': {'http': {'port': '8000'}}}, use_env_vars=True)
    assert isinstance(config['server'], Section)
    assert config['server']['http']['port'] == '9000'


@pytest.mark.parametrize('key,variable', [
    ('dotted.key', 'DOTTED_KEY'), ('space key', 'SPACE_KEY'),
    ('dash-key', 'DASH_KEY'), ('9lives', '_9LIVES'), ('caf\u00e9', 'CAF_'),
])
def test_portable_name_normalization(monkeypatch, key, variable):
    monkeypatch.setenv(variable, 'from environment')
    assert ConfigObj({key: 'file'}, use_env_vars=True)[key] == 'from environment'


def test_prefix_separator_and_case(monkeypatch):
    monkeypatch.setenv('app_mixedCase_X_value_name', 'selected')
    config = ConfigObj({'mixedCase': {'value.name': 'file'}}, use_env_vars=True,
                       env_vars_prefix='app_', env_vars_section_separator='_X_',
                       env_vars_uppercase=False)
    assert config['mixedCase']['value.name'] == 'selected'


def test_empty_and_literal_values_are_not_config_syntax(monkeypatch):
    monkeypatch.setenv('EMPTY', '')
    monkeypatch.setenv('SECRET', 'a,b #not a comment\nsecond line')
    config = ConfigObj({'empty': 'fallback', 'secret': 'fallback'}, use_env_vars=True)
    assert config['empty'] == ''
    assert config['secret'] == 'a,b #not a comment\nsecond line'


def test_unknown_environment_keys_do_not_create_configuration(monkeypatch):
    monkeypatch.setenv('UNRELATED', 'ignore')
    monkeypatch.setenv('NEW__KEY', 'ignore')
    config = ConfigObj({'known': 'file'}, use_env_vars=True)
    assert config.dict() == {'known': 'file'}


def test_schema_declared_values_and_missing_sections(monkeypatch):
    monkeypatch.setenv('PORT', '9000')
    monkeypatch.setenv('SERVER__TLS', 'true')
    spec = ['port = integer(1, 65535)', '[server]', 'tls = boolean', '[absent]', 'value = string']
    config = ConfigObj([], configspec=spec, use_env_vars=True)
    assert config['port'] == '9000'
    assert config['server']['tls'] == 'true'
    assert 'absent' not in config
    result = config.validate(Validator())
    assert result['port'] is True
    assert result['server'] is True
    assert config['port'] == 9000
    assert config['server']['tls'] is True


def test_environment_precedes_schema_default(monkeypatch):
    monkeypatch.setenv('COUNT', '7')
    config = ConfigObj([], configspec=['count = integer(default=3)'], use_env_vars=True)
    assert config.validate(Validator()) is True
    assert config['count'] == 7
    assert 'count' not in config.defaults


def test_repeated_section_uses_actual_name(monkeypatch):
    monkeypatch.setenv('HOSTS__ALPHA__PORT', '9000')
    spec = ['[hosts]', '[[__many__]]', 'port = integer(1, 65535)']
    config = ConfigObj({'hosts': {'alpha': {}, 'beta': {'port': '8000'}}},
                       configspec=spec, use_env_vars=True)
    assert config.validate(Validator()) is True
    assert config['hosts']['alpha']['port'] == 9000
    assert config['hosts']['beta']['port'] == 8000


def test_invalid_override_is_reported_by_normal_validation(monkeypatch):
    monkeypatch.setenv('PORT', 'invalid')
    config = ConfigObj({'port': '8000'}, configspec=['port = integer'], use_env_vars=True)
    errors = flatten_errors(config, config.validate(Validator(), preserve_errors=True))
    assert errors[0][:2] == ([], 'port')
    assert isinstance(errors[0][2], VdtTypeError)


def test_interpolation_uses_effective_values(monkeypatch):
    monkeypatch.setenv('ROOT', '/environment')
    config = ConfigObj(['root = /file', 'path = %(root)s/data'], use_env_vars=True)
    assert config['path'] == '/environment/data'
    config = ConfigObj(['root = /file', 'path = %(root)s/data'],
                       use_env_vars=True, interpolation=False)
    assert config['path'] == '%(root)s/data'


@pytest.mark.parametrize('infile', [
    {'key': 'file'}, ['# preserved', 'key = file # inline'], io.BytesIO(b'key = file\n'),
])
def test_supported_input_sources(monkeypatch, infile):
    monkeypatch.setenv('KEY', 'environment')
    config = ConfigObj(infile, use_env_vars=True)
    assert config['key'] == 'environment'
    if isinstance(infile, dict):
        assert infile['key'] == 'file'
    if isinstance(infile, list):
        assert config.write() == ['# preserved', 'key = environment # inline']


def test_load_snapshot_and_reload(monkeypatch, tmp_path):
    filename = tmp_path / 'settings.ini'
    filename.write_text('key = file\n', encoding='ascii')
    monkeypatch.setenv('APP_KEY', 'first')
    config = ConfigObj(filename, use_env_vars=True, env_vars_prefix='APP_')
    monkeypatch.setenv('APP_KEY', 'second')
    assert config['key'] == 'first'
    config.reload()
    assert config['key'] == 'second'
    monkeypatch.delenv('APP_KEY')
    config.reload()
    assert config['key'] == 'file'
    assert config.env_vars_prefix == 'APP_'
    config.reset()
    assert config.use_env_vars is False
    assert config.env_vars_prefix == ''


def test_schema_is_not_overridden_or_mutated(monkeypatch):
    monkeypatch.setenv('COUNT', '5')
    spec = ConfigObj(['count = integer'], _inspec=True, use_env_vars=True)
    assert spec['count'] == 'integer'
    config = ConfigObj([], configspec=spec, use_env_vars=True)
    assert config.validate(Validator()) is True
    assert config['count'] == 5
    assert spec['count'] == 'integer'


def test_options_dictionary_and_effective_serialization(monkeypatch):
    monkeypatch.setenv('APP_COUNT', '5')
    with pytest.warns(DeprecationWarning):
        config = ConfigObj({'count': '3'}, options={'use_env_vars': True, 'env_vars_prefix': 'APP_'})
    assert config.write() == ['count = 5']


def test_config_content_does_not_enable_environment_mode(monkeypatch):
    monkeypatch.setenv('KEY', 'environment')
    config = ConfigObj(['key = file', '[ConfigObj]', 'use_env_vars = True'])
    assert config['key'] == 'file'


def test_scalar_section_mismatch_still_fails_validation(monkeypatch):
    monkeypatch.setenv('SERVER__PORT', '9000')
    config = ConfigObj({'server': 'invalid'}, configspec=['[server]', 'port = integer'], use_env_vars=True)
    assert config.validate(Validator()) is False
