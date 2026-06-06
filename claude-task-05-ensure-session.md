# Claude Task: Fix Bitwarden _ensure_session Logic

**Project:** Agent Auth Proxy
**Scope:** Single focused fix

**Task:**
Fix the `_ensure_session` method in `app/bitwarden.py` so it correctly detects when the vault is unauthenticated by parsing the JSON output of `bw status`, instead of only checking the exit code.

**Requirements:**
- Parse `bw status --raw` JSON output
- Check for `"status": "unauthenticated"`
- Trigger login when unauthenticated
- Make minimal, targeted changes

Focus only on this fix.