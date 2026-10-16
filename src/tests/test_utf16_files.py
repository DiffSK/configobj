"""UTF-16 files must be decoded before they are split into lines."""
import io
from pathlib import Path
import tempfile
import unittest

from configobj import ConfigObj


class UTF16Files(unittest.TestCase):
    def test_read_utf16_files(self):
        text = 'name = café\n[section]\nvalue = crème\n'
        expected = {'name': 'café', 'section': {'value': 'crème'}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'config.ini'
            for encoding in ('utf-16', 'utf-16-le', 'utf-16-be'):
                data = text.encode(encoding)
                if encoding == 'utf-16-le':
                    data = b'\xff\xfe' + data
                elif encoding == 'utf-16-be':
                    data = b'\xfe\xff' + data
                path.write_bytes(data)
                for explicit in (None, 'utf-16'):
                    for source in (str(path), path, io.BytesIO(data)):
                        with self.subTest(encoding=encoding, explicit=explicit,
                                          source=type(source).__name__):
                            config = ConfigObj(source, encoding=explicit)
                            self.assertEqual(config.dict(), expected)

    def test_written_utf16_file_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'roundtrip.ini'
            config = ConfigObj({'name': 'café'}, encoding='utf-16')
            config.filename = str(path)
            config.write()
            self.assertEqual(ConfigObj(path).dict(), config.dict())
            self.assertEqual(ConfigObj(path, encoding='utf-16').dict(), config.dict())


if __name__ == '__main__':
    unittest.main()
