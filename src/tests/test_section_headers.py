import subprocess
import sys

import pytest

from configobj import ConfigObj, ConfigObjError, NestingError


@pytest.mark.parametrize('line, name, comment', [
    ('[section]', 'section', None),
    ('  [ section ] # comment', 'section', '# comment'),
    ('["  section  "]', '  section  ', None),
    ("['section # ] name'] # tail", 'section # ] name', '# tail'),
    ('[a] b] # tail', 'a] b', '# tail'),
    ('[a] # comment with ] and "', 'a', '# comment with ] and "'),
    ('[a[b]c]', 'a[b]c', None),
    ('[[ ]', '[', None),
    ('[]]', ']', None),
])
def test_section_name_and_comment_grammar(line, name, comment):
    config = ConfigObj([line, 'value = 1'])
    assert config.sections == [name]
    assert config[name]['value'] == '1'
    assert config.inline_comments[name] == comment


def test_spaced_nested_markers_preserve_depth_and_indentation():
    config = ConfigObj(['[parent]', '\t[ [ "child" ] ] # nested', 'value = 1'])
    assert config['parent']['child']['value'] == '1'
    assert config['parent'].inline_comments['child'] == '# nested'
    assert config.indent_type == '\t'


@pytest.mark.parametrize('line', [
    '[section', '["   "]', '[section] trailing',
    '[a\nb]', '["a\nb"]', '[a] # comment\nmore',
])
def test_malformed_section_headers_are_rejected(line):
    with pytest.raises(ConfigObjError):
        ConfigObj([line])


def test_mismatched_markers_still_raise_nesting_error():
    with pytest.raises(NestingError):
        ConfigObj(['[[section]'], raise_errors=True)


@pytest.mark.parametrize('header', [
    "'[a' + '] ' * 50000 + 'b]'",
    "'[\"a' + ' ' * 100000 + 'b\"]'",
])
def test_long_section_headers_complete_without_backtracking(header):
    # Bound regressions in a child so a vulnerable parser cannot hang pytest.
    script = (
        'from configobj import ConfigObj\n'
        'config = ConfigObj([' + header + ', "value = 1"])\n'
        'assert len(config.sections) == 1\n'
        'assert config[config.sections[0]]["value"] == "1"\n'
    )
    subprocess.run([sys.executable, '-c', script], check=True, timeout=5)


def test_long_invalid_header_does_not_backtrack_in_keyword_fallback():
    script = (
        'from configobj import ConfigObj, ConfigObjError\n'
        'try:\n'
        '    ConfigObj(["[name" + " " * 100000 + "invalid"])\n'
        'except ConfigObjError:\n'
        '    pass\n'
        'else:\n'
        '    raise AssertionError("accepted a malformed section")\n'
    )
    subprocess.run([sys.executable, '-c', script], check=True, timeout=5)
