# Bitwarden Integration

## Overview
The proxy uses the Bitwarden CLI (`bw`) exclusively through `app/bitwarden.py`.

## Key Features
- Session management with automatic re-auth
- Advanced error handling and sanitization
- Collection-based access control

## Error Handling
All Bitwarden errors are mapped to safe internal error codes.