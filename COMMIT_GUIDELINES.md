# GitSquisher Commit Message Guidelines

## Quick Rule (use this every time)
<type>: <short description>

### Allowed types (lowercase)
- feat     → new feature (button, squish option, etc.)
- fix      → bug fix
- chore    → build, tooling, cleanup, or maintenance
- docs     → documentation only
- style    → formatting, whitespace, comments
- refactor → code improvement that changes nothing externally
- test     → adding or updating tests

### Examples (exactly how you should commit)
git commit -m "feat: add one-click Encrypt & Key button"
git commit -m "chore: apply advanced .gitignore template on load"
git commit -m "fix: prevent squishes/ folder from being zipped inside itself"
git commit -m "docs: update COMMIT_GUIDELINES.md with clearer examples"

## Simple Rules to Follow
1. First line must be 50 characters or less.
2. Use present tense (“add button”, not “added button”).
3. No period at the end of the subject line.
4. Be specific but concise.
5. If you need more detail, add a blank line and write a longer body.

## Quick command to remember
git commit -m "type: what you changed"

Follow these and your Git history will stay clean, readable, and professional forever.
