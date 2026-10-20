"""Decoded config files split only at physical CR/LF line boundaries."""
from pathlib import Path
import tempfile
import unittest

from configobj import ConfigObj


class UnicodeLineSeparatorsInValues(unittest.TestCase):
    expected = {
        'form_feed': 'left\fright',
        'unicode_separator': 'north\u2028south',
    }

    def _check_file(self, path, encoding):
        for source in (str(path), path):
            for explicit_encoding in (None, encoding):
                with self.subTest(source=type(source).__name__,
                                  encoding=explicit_encoding):
                    config = ConfigObj(source, encoding=explicit_encoding)
                    self.assertEqual(config.dict(), self.expected)

    def _check_encoding(self, encoding, newlines):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'values.ini'
            for newline in newlines:
                with self.subTest(file_encoding=encoding, newline=repr(newline)):
                    text = ('form_feed = left\fright{0}'
                            'unicode_separator = north\u2028south{0}').format(newline)
                    path.write_bytes(text.encode(encoding))
                    self._check_file(path, encoding)

    def test_utf8_values_can_contain_non_line_separators(self):
        # These physical line endings already work on the release base.
        self._check_encoding('utf-8', ('\n', '\r\n'))

    def test_utf16_values_can_contain_non_line_separators(self):
        self._check_encoding('utf-16', ('\n', '\r\n'))

    def test_bare_carriage_return_remains_a_line_ending(self):
        # The current PR candidate accepts bare CR; don't regress that behavior.
        for encoding in ('utf-8', 'utf-16'):
            with self.subTest(file_encoding=encoding):
                self._check_encoding(encoding, ('\r',))


if __name__ == '__main__':
    unittest.main()
