# Evidence Workspace

Use this folder for raw or lightly cleaned evidence that supports research claims.

Recommended layout:

- `commands/` for terminal transcripts, versions, install notes, and failure output.
- `repo_metadata/` for release, license, commit, contributor, and issue snapshots.
- `docs/` for short notes about official documentation pages.
- `screenshots/` for UI or terminal screenshots when useful.
- `fixtures/` for synthetic datasets and example inputs.

Evidence files should be named with the date, tool name, and evidence type when possible:

```text
MM-DD-YYYY_tool-name_evidence-type.md
MM-DD-YYYY_tool-name_command-output.txt
MM-DD-YYYY_tool-name_release-snapshot.md
```

Do not store real taxpayer data, real financial account data, personally identifiable information, secrets, or live filing credentials here.
