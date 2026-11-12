import unittest

from detection.analyzer import PIIAnalyzer
from detection.validators import is_valid_credit_card, is_valid_ssn


class DetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.analyzer = PIIAnalyzer()

    def test_detects_common_identifiers(self) -> None:
        text = (
            "Contact alex@example.com or +1 (415) 555-0132. "
            "SSN 123-45-6789, IP 192.0.2.10, employee EMP-12345."
        )
        findings = self.analyzer.analyze(text)
        self.assertEqual(
            [finding.entity_type for finding in findings],
            ["EMAIL", "PHONE", "SSN", "IP_ADDRESS", "EMPLOYEE_ID"],
        )
        self.assertEqual(
            [finding.text for finding in findings],
            [
                "alex@example.com",
                "+1 (415) 555-0132",
                "123-45-6789",
                "192.0.2.10",
                "EMP-12345",
            ],
        )

    def test_validates_credit_card_checksum_and_ssn_groups(self) -> None:
        self.assertTrue(is_valid_credit_card("4111 1111 1111 1111"))
        self.assertFalse(is_valid_credit_card("4111 1111 1111 1112"))
        self.assertTrue(is_valid_ssn("123-45-6789"))
        self.assertFalse(is_valid_ssn("000-12-3456"))

    def test_ignores_invalid_candidates(self) -> None:
        findings = self.analyzer.analyze(
            "Email nobody@invalid and invalid SSN 000-00-0000."
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
