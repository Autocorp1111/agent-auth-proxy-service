# Claude Task: Real Bitwarden Connectivity Check

**Project:** /mnt/e/Agents/project/agent-auth-proxy
**Scope:** Single focused improvement

**Task:**
Update the `/ready` (or health) endpoint so it actually tests Bitwarden connectivity instead of just checking if the client object exists.

**Requirements:**
- Perform a lightweight check (e.g. `bw status` or a simple vault query)
- Return proper status based on whether Bitwarden is reachable
- Make minimal changes to `app/routes/health.py`
- Keep the endpoint fast and non-blocking where possible

Focus only on making the health check meaningful.