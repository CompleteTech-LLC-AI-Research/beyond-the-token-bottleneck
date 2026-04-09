# Schema Self-Audit

```mermaid
graph TD
    A[Compare Directory Structure] --> B[Compare MOC List]
    B --> C[Check 5+ Page Themes]
    C --> D[Verify Frontmatter Templates]
    D --> E[Verify Workflow References]
    E --> F[Report Findings]
    F --> G{User Approval?}
    G -->|Yes| H[Apply Fixes]
    H --> I[Log in wiki/log.md]
    I --> J[Commit & Push]
    J --> K[Report Outcome]
    G -->|No| L[End Without Changes]

    style A fill:#dae8fc,stroke:#6c8ebf,color:#333
    style B fill:#fff2cc,stroke:#d6b656,color:#333
    style C fill:#fff2cc,stroke:#d6b656,color:#333
    style D fill:#d5e8d4,stroke:#82b366,color:#333
    style E fill:#ffe6cc,stroke:#d79b00,color:#333
    style F fill:#e1d5e7,stroke:#9673a6,color:#333
    style G fill:#fff2cc,stroke:#d6b656,color:#333
    style H fill:#e1d5e7,stroke:#9673a6,color:#333
    style I fill:#d5e8d4,stroke:#82b366,color:#333
    style J fill:#dae8fc,stroke:#6c8ebf,color:#333
    style K fill:#d5e8d4,stroke:#82b366,color:#333
    style L fill:#f8cecc,stroke:#b85450,color:#333
```

## Purpose

Verify that `AGENTS.md` still matches the real vault layout, current MOC inventory, workflow references, and the frontmatter fields used by existing pages.

## When To Use

- The vault structure changes.
- Workflow files are added, moved, or refactored.
- MOCs are created or removed.
- Frontmatter templates may be stale.
- You need a periodic consistency check on the schema itself.

## Trigger Phrases

- `schema self-audit`
- `audit AGENTS.md`
- `verify workflow references`
- `check the schema`
- `sync the schema with the vault`

## Do Not Use When

- You only need to add a new page or update content.
- You are doing a normal ingest, expand, or synthesis task.
- You are already in a narrower workflow that will naturally update the affected references.

## Required Context

- The current vault directory structure.
- The actual `wiki/mocs/*.md` files.
- The current workflow files and their paths.
- The frontmatter fields used by real pages.

## Procedure

1. Compare the directory structure listing in `AGENTS.md` (the 'Directory Layout' section) against the actual filesystem using `ls -R wiki/` and `ls -R workflows/`.
2. Compare the `Current MOCs` list against the actual `wiki/mocs/*.md` files.
3. Check whether any theme has accumulated `5+` pages without a MOC, which should trigger `MOC Gap Analysis`.
4. Verify that frontmatter templates include every field actually used in existing pages.
5. Verify that all workflow file references in `AGENTS.md`'s 'Workflow Index' section point to files that exist on disk using `Glob`.
6. Report all findings from steps 1–5.
7. Apply fixes only with user approval. If step 3 identifies a 5+ page cluster without a MOC, note this for a future [MOC Gap Analysis](moc-gap-analysis.md) run.
8. Log the schema self-audit in `wiki/log.md`.
9. Run [commit and push](../_shared/procedures/commit-and-push.md) in full, then return here and continue with step 10. Research-bucket fixes go to `master`; if this run also touched workflow files, those go via PR per the fragment's split.
10. Report the outcome to the user.

## Completion Checklist

- All items in [`../_shared/checklists/base.md`](../_shared/checklists/base.md) hold.
- All items in [`../_shared/checklists/audit-additions.md`](../_shared/checklists/audit-additions.md) hold.
- `AGENTS.md` matches the actual vault directory structure.
- `AGENTS.md` lists the actual MOC files.
- Workflow references point to real files.
- Frontmatter templates reflect the fields used in the vault.
- Any discovered drift was corrected.

## Related Workflows

- `workflows/audit/moc-gap-analysis.md` for coverage gaps in navigation.
- `workflows/audit/review.md` for broader wiki-wide validation.
- `workflows/enrich/enrich.md` for structural cleanup after drift is found.
