# Claude Task: Fix Auth Performance (Linear Scan)

**Project:** Agent Auth Proxy
**Scope:** Performance & security fix

**Task:**
Fix the `get_current_agent` function so it doesn't do a full table scan + N bcrypt checks on every request.

**Requirements:**
- Add a `key_prefix` column (first 8-10 chars of the raw API key)
- Query using the prefix first to narrow to 1 row
- Then do a single bcrypt check
- Make the change in `app/database.py` (model) and `app/auth.py`

Focus on this performance fix.