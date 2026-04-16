REPORT_DESCRIPTION = """
Aggregates all classified changes.
Computes severity counts.
Determines risk signal:
- REJECT if any CRITICAL changes.
- REVIEW if more than 3 MODERATE changes.
- PASS otherwise.
"""
