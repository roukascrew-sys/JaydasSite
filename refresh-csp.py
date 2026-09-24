#!/usr/bin/env python3
"""Refresh the embedded script allowlist after editing this standalone HTML.
Usage: python3 refresh-csp.py cramers-customlights.html
No third-party Python packages required. Review edits before running.
"""
import base64
import hashlib
from pathlib import Path
import re
import sys
path = Path(sys.argv[1] if len(sys.argv) > 1 else 'cramers-customlights.html')
html = path.read_text(encoding='utf-8')
hashes = ["'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode('utf-8')).digest()).decode() + "'"
          for m in re.finditer(r'<script\b[^>]*>(.*?)</script>', html, re.S)]
policy = "default-src 'none'; script-src " + ' '.join(hashes) + "; style-src 'unsafe-inline'; font-src data:; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-src 'none'"
html, count = re.subn(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">',
                     lambda _: '<meta http-equiv="Content-Security-Policy" content="' + policy + '">', html, count=1)
if count != 1:
    raise SystemExit('Expected exactly one existing CSP meta tag; no file written.')
path.write_text(html, encoding='utf-8')
print('Updated script hashes. Re-test the page before publishing.')
