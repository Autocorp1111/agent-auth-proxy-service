# Architecture - Agent Auth Proxy

## Overview
The Agent Auth Proxy acts as a secure intermediary between AI agents and Bitwarden.

## Components
- **FastAPI Application**: Main entry point
- **Bitwarden Client**: Handles all `bw` CLI interactions
- **Database Layer**: SQLAlchemy async models for agents and access logs
- **Authentication**: API key-based auth with bcrypt hashing

## Data Flow
1. Agent authenticates with API key
2. Request is validated
3. Access check against `credential_access` table
4. Bitwarden client retrieves credential
5. Access is logged

## Security Considerations
- Only one module touches the Bitwarden CLI
- All access is audited
- Credentials are never cached in plaintext