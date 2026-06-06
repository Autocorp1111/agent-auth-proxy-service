# Claude Task: Set X-Request-ID

**Project:** Agent Auth Proxy
**Scope:** Single focused improvement

**Task:**
Ensure the `X-Request-ID` header is actually set on responses by the middleware.

**Requirements:**
- Generate a UUID for each request if not provided
- Store it in `request.state.request_id`
- Add it to the response headers
- Make minimal changes to `app/main.py`

Focus only on this.