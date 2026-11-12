import unittest

from core.anonymizer import Anonymizer
from core.restoration import restore_tokens
from core.token_vault import TokenVault
from detection.analyzer import PIIAnalyzer


class AnonymizerTests(unittest.TestCase):
    def test_anonymizes_and_restores_repeated_values(self) -> None:
        text = "Email alex@example.com, then contact alex@example.com."
        findings = PIIAnalyzer().analyze(text)
        vault = TokenVault()

        anonymized = Anonymizer().anonymize(text, findings, vault)

        self.assertEqual(
            anonymized,
            "Email <EMAIL_1>, then contact <EMAIL_1>.",
        )
        self.assertEqual(restore_tokens(anonymized, vault), text)
        self.assertEqual(len(vault), 1)

    def test_anonymizer_leaves_unmatched_text_unchanged(self) -> None:
        text = "No identifiers here."
        self.assertEqual(Anonymizer().anonymize(text, [], TokenVault()), text)


if __name__ == "__main__":
    unittest.main()
