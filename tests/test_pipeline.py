import json
import tempfile
import unittest
from pathlib import Path

from audit.audit_view import load_audit_records
from audit.logger import AuditLogger
from core.pipeline import PrivacyPipeline


class PipelineTests(unittest.TestCase):
    def test_pipeline_anonymizes_verifies_and_restores(self) -> None:
        source = "Email alex@example.com and call +1 (415) 555-0132."
        result = PrivacyPipeline().process(source)

        self.assertTrue(result.verification.is_safe)
        self.assertNotIn("alex@example.com", result.anonymized_text)
        self.assertNotIn("415", result.anonymized_text)
        self.assertEqual(PrivacyPipeline.restore(result.anonymized_text, result), source)

    def test_audit_contains_counts_but_not_source_values(self) -> None:
        source = "Email alex@example.com."
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_path = Path(temp_dir) / "audit.jsonl"
            result = PrivacyPipeline(
                audit_logger=AuditLogger(audit_path)
            ).process(source)

            records = load_audit_records(audit_path)
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["entity_counts"], {"EMAIL": 1})
            self.assertTrue(records[0]["verified"])
            self.assertNotIn("alex@example.com", audit_path.read_text(encoding="utf-8"))
            self.assertTrue(result.verification.is_safe)

    def test_audit_records_are_valid_json_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            audit_path = Path(temp_dir) / "audit.jsonl"
            AuditLogger(audit_path).log_processing({"EMAIL": 2}, verified=True)
            record = json.loads(audit_path.read_text(encoding="utf-8"))
            self.assertEqual(record["event"], "text_processed")


if __name__ == "__main__":
    unittest.main()
