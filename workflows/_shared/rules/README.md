# Rule fragments

Invariants and constraints the wiki must maintain at all times, independent of which workflow is currently running. Rules are the "must never" and "must always" statements that any workflow can assume hold before it starts and must leave holding when it finishes.

Examples of the kind of rules that will live here:

- Never reference a path without verifying it exists on disk.
- Never backdate log entries; timestamps are append-only.
- Never introduce a MOC entry for a note that does not exist.
- Never rename a source without updating every backlink in the same commit.

Rule bodies land in PR 2; this PR only establishes the directory.
