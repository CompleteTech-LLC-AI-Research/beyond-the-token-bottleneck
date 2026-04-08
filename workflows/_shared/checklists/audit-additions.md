# Audit Completion Additions

## Purpose

The completion items specific to workflows that audit the wiki without (necessarily) creating new content: `lint.md`, `review.md`, `enrichment-audit.md`, `verification.md`, `schema-self-audit.md`, and `plugin-audit.md`. Compose with [`base.md`](base.md) — both must hold for an audit-class workflow to be considered complete.

## When to use

- At the end of any audit-class workflow run.
- After applying audit-found fixes, to confirm the audit's findings list is fully resolved.

## The audit additions

- [ ] **Findings are grouped by class** (content vs structural for lint, depth vs link for enrichment-audit, factual vs overstatement vs missing-coverage for verification). Mixed-class findings hide patterns.
- [ ] **Proposed fixes are specific and actionable** — file path + line number + exact change, not "the page needs work". A finding without a fix is a deferred TODO, not a finding.
- [ ] **No silent fixes were applied during the audit pass.** Audit workflows flag findings; the user (or a follow-up workflow run) approves and applies. Silent fixes hide error patterns and prevent learning where drift clusters.
- [ ] **Fixes were applied only after user approval**, in the priority order documented by the workflow (factual errors → overstatements → missing coverage → style for verification; high → medium → low for enrichment-audit).
- [ ] **The escalation rule was honored** if the audit included a parallel-subagent phase. Per [`../procedures/spot-check-agent-output.md`](../procedures/spot-check-agent-output.md): 2+ issues across the spot-check sample → full verification pass before consolidation.
- [ ] **The log entry mentions which class of finding fired**, not just "ran the audit". Future audit passes can grep the log to track which classes drift fastest.
- [ ] **If the audit revealed terminology drift**, the canonical terms in [`../glossary.md`](../glossary.md) were applied (or the drift was added to the audit's findings list for the user to apply).
- [ ] **No coordinator-only files were edited by review subagents** if any were dispatched. The protocol in [`../procedures/parallel-subagent-protocol.md`](../procedures/parallel-subagent-protocol.md) is non-negotiable for audit workflows that fan out to subagents (verification's read-only review agents are a special case but the rule still applies).

## Used by

- `workflows/audit/lint.md`
- `workflows/audit/review.md`
- `workflows/audit/enrichment-audit.md`
- `workflows/audit/verification.md`
- `workflows/audit/schema-self-audit.md`
- `workflows/audit/plugin-audit.md`
