# Claude Task: Set Up Alembic Properly

**Project:** Agent Auth Proxy
**Scope:** Infrastructure fix

**Task:**
Create proper Alembic configuration so migrations can actually be run.

**Requirements:**
- Ensure `alembic.ini` is correctly configured
- Create or fix `alembic/env.py` to work with the SQLAlchemy models
- Make sure `alembic upgrade head` works

Focus only on making Alembic functional.