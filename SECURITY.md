# Security and Privacy

Raw Android `logcat` output from CFMOTO RIDE can contain sensitive information.

Potentially sensitive fields include:

- authentication / bearer tokens
- user or account IDs
- vehicle identifiers
- exact GPS history
- timestamps
- device information

## Do not upload raw ride captures to a public GitHub repository

The included `.gitignore` excludes common capture filenames, but `.gitignore` is not a substitute for checking what you commit.

Before running:

```bash
git add .
```

review the directory and make sure no personal ride capture, token, GPX, or account-specific file is being published.

Use this workflow only with accounts and data you are authorized to access.
