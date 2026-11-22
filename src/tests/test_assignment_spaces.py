import io

import pytest

from configobj import ConfigObj


def test_compact_assignments_preserve_values_comments_and_nested_sections():
    source = [
        'root = "keep = spaces" # root comment',
        '[section]',
        '    items = one, two',
        '    [[child]]',
        '        text = "a = b"',
    ]
    config = ConfigObj(source)
    config.indent_type = '    '
    before = config.write()
    compact = config.write(spaces=False)
    assert compact == [
        'root=keep = spaces     # root comment',
        '[section]',
        '    items=one, two',
        '    [[child]]',
        '        text=a = b',
    ]
    assert ConfigObj(compact) == config
    assert config.write() == before
    assert config.write(spaces=True) == before


def test_compact_assignments_preserve_multiline_values():
    config = ConfigObj({'value': 'first = line\nsecond = line'})
    lines = config.write(spaces=False)
    assert lines[0].startswith('value=')
    assert 'first = line\nsecond = line' in lines[0]
    assert ConfigObj('\n'.join(lines).splitlines()) == config


@pytest.mark.parametrize('target', ['lines', 'stream', 'file'])
def test_compact_assignments_support_encoded_output(tmp_path, target):
    config = ConfigObj({'section': {'name': 'caf\u00e9'}},
                       encoding='utf-8', indent_type='  ')
    config.newlines = '\n'
    expected = '[section]\n  name=caf\u00e9\n'.encode('utf-8')
    if target == 'lines':
        assert b'\n'.join(config.write(spaces=False)) + b'\n' == expected
    elif target == 'stream':
        output = io.BytesIO()
        config.write(output, spaces=False)
        assert output.getvalue() == expected
    else:
        config.filename = str(tmp_path / 'compact.ini')
        config.write(spaces=False)
        assert (tmp_path / 'compact.ini').read_bytes() == expected


def test_compact_assignments_support_unrepr_and_quoted_keys():
    config = ConfigObj(unrepr=True)
    config['#key'] = (1, 'a = b')
    lines = config.write(spaces=False)
    assert lines == ['"#key"=(1, \'a = b\')']
    assert ConfigObj(lines, unrepr=True) == config
