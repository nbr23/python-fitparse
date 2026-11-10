import json
import os
import tempfile
import unittest

from fitparse import fitdump

ACTIVITY = os.path.join(os.path.dirname(__file__), 'files', 'garmin-edge-500-activity.fit')


class FitdumpTestCase(unittest.TestCase):
    def dump(self, *args):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, 'out')
            fitdump.main(['-o', out, *args, ACTIVITY])
            with open(out, encoding='utf-8') as f:
                return f.read()

    def test_readable(self):
        output = self.dump()
        self.assertIn('. file_id\n', output)
        self.assertIn('. record\n', output)

    def test_json(self):
        messages = json.loads(self.dump('-t', 'json'))
        self.assertTrue(messages)
        self.assertIn('record', {m['type'] for m in messages})

    def test_gpx(self):
        output = self.dump('-t', 'gpx')
        self.assertIn('<trkpt', output)
        self.assertTrue(output.endswith('</gpx>\n'))

    def test_name_filter(self):
        messages = json.loads(self.dump('-t', 'json', '-n', 'record'))
        self.assertTrue(messages)
        self.assertEqual({m['type'] for m in messages}, {'record'})


if __name__ == '__main__':
    unittest.main()
