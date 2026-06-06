# Claude Code Task: Milestone 1 - Bitwarden Validation Gate

## Goal
Complete the hard gate for Milestone 1 by implementing and validating Steps 0–6 for the Bitwarden CLI integration on Railway.

## Context
- The `bitwarden.py` module is already implemented with advanced error handling.
- `validate_bitwarden_gate.py` script exists in `scripts/`.
- The service is currently deployed on Railway but has had start command issues.
- `railway.toml` now contains an explicit `startCommand`.

## Requirements
1. Ensure the validation script runs successfully in the Railway environment.
2. Verify all Steps 0–6 pass.
3. Document any issues found during validation.
4. Confirm the Bitwarden client works end-to-end with the current implementation.

## Steps to Perform
1. Run the validation script in Railway shell:
   ```bash
   python scripts/validate_bitwarden_gate.py
   ```
2. Fix any issues that prevent the script from passing.
3. Once all steps pass, update this task with results.

## Acceptance Criteria
- All Steps 0–6 return PASS
- No unhandled Bitwarden CLI errors
- The service can successfully fetch at least one credential

## Output
When complete, reply with:
- Validation results
- Any code changes made
- Confirmation that the hard gate is cleared

## Notes
- Only modify files inside `app/` and `scripts/`
- Do not proceed to Milestone 2 until this gate is passed
