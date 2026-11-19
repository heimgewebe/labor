from __future__ import annotations

from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generate_doc_index


class DocIndexScratchTests(unittest.TestCase):
    def test_model_lab_test_scratch_is_not_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = {
                "tests/fixtures/model_lab_condition_design/_scratch_123/stale.md": False,
                "tests/fixtures/model_lab_condition_design/valid/bundle/common-condition.md": True,
                "tests/fixtures/model_lab_condition_design/not_scratch/still-current.md": True,
                "tests/fixtures/other_lab/_scratch_123/unrelated.md": True,
                "docs/guide.md": True,
            }
            for name in cases:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Test document\n", encoding="utf-8")

            output = root / "docs/_generated/doc-index.md"
            with (
                patch.object(generate_doc_index, "REPO_ROOT", root),
                patch.object(generate_doc_index, "OUTPUT", output),
                redirect_stdout(io.StringIO()),
            ):
                generate_doc_index.main()

            rendered = output.read_text(encoding="utf-8")
            for name, expected in cases.items():
                with self.subTest(path=name):
                    self.assertEqual(expected, f"| `{name}` |" in rendered)


if __name__ == "__main__":
    unittest.main()
