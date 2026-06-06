# Error Codes

| Code | Meaning                        | Common Causes                     |
|------|--------------------------------|-----------------------------------|
| 401  | Unauthorized                   | Invalid or missing API key        |
| 403  | Forbidden                      | Agent does not have access        |
| 422  | Validation Error               | Invalid request body              |
| 429  | Too Many Requests              | Rate limit exceeded               |
| 503  | Service Unavailable            | Bitwarden CLI error               |
| 500  | Internal Server Error          | Unexpected error                  |