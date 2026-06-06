# Claude Task: Fix Admin Authorization

**Project:** /mnt/e/Agents/project/agent-auth-proxy
**Scope:** Single focused fix

**Task:**
Fix the `get_admin_agent` function in `app/auth.py` so that it properly validates against `ADMIN_API_KEY` from settings instead of just checking `is_active`.

**Requirements:**
- Use the existing `ADMIN_API_KEY` from `app/config.py`
- Keep the function signature compatible with FastAPI dependencies
- Make minimal, targeted changes
- After the fix, briefly confirm what was changed

Do not work on any other files or issues.