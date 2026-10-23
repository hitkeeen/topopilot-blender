import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

from topopilot.cli import main


class CliTests(unittest.TestCase):
    def test_sample_outputs_json(self):
        output = StringIO()
        with redirect_stdout(output):
            result = main(["diagnose", "--sample"])
        self.assertEqual(result, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["schema_version"], "1")
        self.assertIn("warnings", payload)

    def test_output_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            self.assertEqual(main(["diagnose", "--sample", "--output", path]), 0)
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["name"], "sample_mesh")


if __name__ == "__main__":
    unittest.main()
