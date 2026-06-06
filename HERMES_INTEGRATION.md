# Hermes Integration Guide

## Overview
This document describes how Hermes agents should connect to the Agent Auth Proxy.

## Configuration
Hermes should store the proxy URL and its API key in its configuration.

## Usage
When Hermes needs a credential, it calls:
`GET /credentials/{name}` with its Bearer token.

## Benefits
- Centralized credential management
- Full audit trail
- No direct Bitwarden access from individual agents