"""A failed save must not truncate a user's existing configuration."""

import io
import os
import stat

import pytest

from configobj import ConfigObj
from configobj import _atomic


@pytest.fixture
def config(tmp_path):
    destination = tmp_path / 'settings.ini'
    destination.write_bytes(b'value = old\n')
    result = ConfigObj(destination)
    result['value'] = 'new'
    return result


def assert_original(config):
    filename = config.filename
    with open(filename, 'rb') as stream:
        assert stream.read() == b'value = old\n'
    assert sorted(os.listdir(os.path.dirname(filename))) == ['settings.ini']


def test_complete_file_is_synced_before_replacement(config, monkeypatch):
    replace = os.replace
    fsync = os.fsync
    synced = []

    def record_sync(fd):
        synced.append(fd)
        fsync(fd)

    def check_replace(source, destination):
        assert synced
        assert os.path.dirname(source) == os.path.dirname(destination)
        with open(destination, 'rb') as stream:
            assert stream.read() == b'value = old\n'
        with open(source, 'rb') as stream:
            assert stream.read() == b'value = new\n'
        replace(source, destination)

    monkeypatch.setattr(_atomic.os, 'fsync', record_sync)
    monkeypatch.setattr(_atomic.os, 'replace', check_replace)
    assert config.write() is None
    assert ConfigObj(config.filename)['value'] == 'new'
    assert os.listdir(os.path.dirname(config.filename)) == ['settings.ini']


@pytest.mark.parametrize('operation', ['open', 'fdopen', 'chmod', 'fsync', 'replace'])
def test_failure_keeps_original_and_cleans_temporary(config, monkeypatch, operation):
    def fail(*args, **kwargs):
        raise OSError('injected ' + operation + ' failure')

    monkeypatch.setattr(_atomic.os, operation, fail)
    with pytest.raises(OSError, match='injected ' + operation):
        config.write()
    assert_original(config)


@pytest.mark.parametrize('operation', ['write', 'flush', 'close'])
def test_stream_failure_keeps_original(config, monkeypatch, operation):
    fdopen = os.fdopen

    class FailingStream:
        def __init__(self, fd, mode):
            self.stream = fdopen(fd, mode)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.stream.close()
            if operation == 'close':
                raise OSError('injected close failure')

        def write(self, content):
            if operation == 'write':
                self.stream.write(content[:3])
                raise OSError('injected write failure')
            return self.stream.write(content)

        def flush(self):
            if operation == 'flush':
                raise OSError('injected flush failure')
            return self.stream.flush()

        def fileno(self):
            return self.stream.fileno()

    monkeypatch.setattr(_atomic.os, 'fdopen', FailingStream)
    with pytest.raises(OSError, match='injected ' + operation):
        config.write()
    assert_original(config)


def test_failed_new_file_does_not_leave_empty_destination(tmp_path, monkeypatch):
    config = ConfigObj({'value': 'new'})
    config.filename = tmp_path / 'new.ini'

    def fail(*args):
        raise OSError('injected replacement failure')

    monkeypatch.setattr(_atomic.os, 'replace', fail)
    with pytest.raises(OSError, match='injected replacement'):
        config.write()
    assert list(tmp_path.iterdir()) == []


def test_encoding_failure_leaves_original(config):
    config['value'] = '\u96ea'
    with pytest.raises(UnicodeEncodeError):
        config.write()
    assert_original(config)


@pytest.mark.parametrize('encoding,bom', [('utf-8', True), ('utf-16', False), ('utf-8', False)])
def test_atomic_output_matches_stream_bytes(tmp_path, encoding, bom):
    config = ConfigObj({'value': '\u96ea', 'nested': {'answer': '42'}}, encoding=encoding)
    config.newlines = '\r\n'
    config.BOM = bom
    config.initial_comment = ['# keep this comment']
    output = io.BytesIO()
    config.write(output)
    config.filename = tmp_path / 'settings.ini'
    config.write()
    assert config.filename.read_bytes() == output.getvalue()
    assert ConfigObj(io.BytesIO(config.filename.read_bytes()), encoding=encoding) == config


def test_symlink_keeps_link_and_updates_target(tmp_path):
    directory = tmp_path / 'target'
    directory.mkdir()
    target = directory / 'settings.ini'
    target.write_bytes(b'value = old\n')
    link = tmp_path / 'linked.ini'
    try:
        link.symlink_to('target/settings.ini')
    except OSError as error:
        pytest.skip('Symlinks unavailable: ' + str(error))
    config = ConfigObj(str(link))
    config.newlines = '\n'
    config['value'] = 'new'
    config.write()
    assert link.is_symlink()
    assert target.read_bytes() == b'value = new\n'
    assert list(directory.iterdir()) == [target]


def test_file_like_output_never_replaces_filename(config, monkeypatch):
    def fail(*args):
        pytest.fail('File-like output must not replace a filename')

    monkeypatch.setattr(_atomic, 'atomic_write', fail)
    stream = io.BytesIO()
    config.write(stream)
    assert stream.getvalue() == b'value = new\n'
    assert_original(config)
    config.filename = None
    assert config.write() == ['value = new']


def test_rejects_non_regular_file(tmp_path):
    destination = tmp_path / 'directory'
    destination.mkdir()
    config = ConfigObj({'value': 'new'})
    config.filename = destination
    with pytest.raises(OSError, match='regular file'):
        config.write()
    assert destination.is_dir()
    assert list(tmp_path.iterdir()) == [destination]


def test_existing_permissions_are_preserved(config):
    mode = 0o640 if os.name == 'posix' else stat.S_IREAD | stat.S_IWRITE
    os.chmod(config.filename, mode)
    before = stat.S_IMODE(os.stat(config.filename).st_mode)
    config.write()
    assert stat.S_IMODE(os.stat(config.filename).st_mode) == before


@pytest.mark.skipif(os.name != 'posix', reason='POSIX umask semantics')
def test_new_file_obeys_umask(tmp_path):
    config = ConfigObj({'value': 'new'})
    config.filename = tmp_path / 'settings.ini'
    previous = os.umask(0o027)
    try:
        config.write()
    finally:
        os.umask(previous)
    assert stat.S_IMODE(config.filename.stat().st_mode) == 0o640


@pytest.mark.skipif(os.name != 'nt', reason='Windows read-only replacement semantics')
def test_readonly_failure_cleans_readonly_temporary(config):
    os.chmod(config.filename, stat.S_IREAD)
    try:
        with pytest.raises(PermissionError):
            config.write()
        assert_original(config)
    finally:
        os.chmod(config.filename, stat.S_IREAD | stat.S_IWRITE)


@pytest.mark.skipif(os.name != 'posix', reason='POSIX directory fsync')
def test_directory_sync_failure_reports_complete_replacement(config, monkeypatch):
    fsync = os.fsync

    def fail_directory(fd):
        if stat.S_ISDIR(os.fstat(fd).st_mode):
            raise OSError('directory sync failure')
        fsync(fd)

    monkeypatch.setattr(_atomic.os, 'fsync', fail_directory)
    with pytest.raises(OSError, match='directory sync failure'):
        config.write()
    assert ConfigObj(config.filename)['value'] == 'new'
    assert os.listdir(os.path.dirname(config.filename)) == ['settings.ini']
