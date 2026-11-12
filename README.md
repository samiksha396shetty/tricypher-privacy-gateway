<<<<<<< HEAD
# TriCypher Privacy Gateway

A small Streamlit demo that detects common personal identifiers locally, replaces
them with request-scoped tokens, verifies the sanitized text, and optionally
sends only verified anonymized text to an OpenAI-compatible chat-completions API.

## Project layout

- `core/`: anonymization, token storage, verification, processing pipeline, and optional LLM client.
- `detection/`: local recognizers and validation helpers.
- `ui/`: Streamlit dashboard and reusable components.
- `audit/`: JSON Lines audit logging and dashboard reader.
- `datasets/`: synthetic examples and expected entity labels.
- `tests/`: unit tests for detection, anonymization, and the pipeline.

## Run locally

Use Python 3.10 or newer:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

LLM use is optional. Copy `.env.example` to `.env`, add an API key, and configure
the endpoint/model if needed. The dashboard reads `LLM_API_KEY`,
`LLM_BASE_URL`, and `LLM_MODEL` from the process environment or `.env`. The
gateway does not send source text to the provider.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Detection and privacy notes

Detection is local and rule-based. It covers email addresses, US-style phone
numbers, SSNs, Luhn-valid payment-card numbers, IPv4 addresses, API-key-shaped
strings, and `EMP-` employee IDs. This is a demo, not a complete DLP solution:
it can miss sensitive data, and pattern detection can produce false positives.
Review the anonymized output before sharing it.

Tokens are reversible only through an in-memory vault attached to a single
pipeline result. Do not persist or expose that vault. The audit file records only
timestamps, entity counts, and verification status; it never records source text.
An external LLM provider may retain requests under its own policies.
=======
# tricypher-privacy-gateway
>>>>>>> 5766aa54da4e67c451d370c04ca71b0a3330b2cf
