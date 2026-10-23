import json
import unittest
from pathlib import Path

from topopilot.diagnosis import diagnose_mesh


FIXTURE = Path(__file__).parents[1] / "topopilot" / "fixtures" / "sample_mesh.json"


class DiagnosisTests(unittest.TestCase):
    def test_sample_reports_expected_issues(self):
        report = diagnose_mesh(json.loads(FIXTURE.read_text(encoding="utf-8")), "sample_mesh")
        self.assertEqual(report["schema_version"], "1")
        self.assertEqual(report["metrics"]["face_count"], 9)
        self.assertEqual(report["metrics"]["degenerate_face_count"], 1)
        self.assertIn("boundary_edges", report["warnings"])
        self.assertIn("degenerate_faces", report["warnings"])
        self.assertEqual(report["metrics"]["unused_vertex_count"], 1)

    def test_closed_tetrahedron_has_no_boundary_edges(self):
        mesh = {"vertices": [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], "faces": [[0, 2, 1], [0, 1, 3], [1, 2, 3], [2, 0, 3]]}
        report = diagnose_mesh(mesh)
        self.assertEqual(report["metrics"]["boundary_edge_count"], 0)
        self.assertEqual(report["warnings"], [])


if __name__ == "__main__":
    unittest.main()
