# ADR-002: Use profile-driven CV variants

## Status

Accepted

## Context

A job seeker needs several versions of the same CV. Duplicating complete source files causes drift: a change to a role, contact detail, or skill must be repeated manually and can become inconsistent.

## Decision

Keep reusable professional data separate from job-specific profiles. A profile selects, excludes, and prioritizes content and can reference localized Markdown text. The build command accepts a profile name and language.

## Alternatives considered

### Duplicate complete CVs

Rejected because duplicated content is difficult to keep consistent and is not a good target for AI-assisted maintenance.

### Git branches as the primary variant mechanism

Rejected as the user-facing data model. Branches may still be useful for advanced workflows, but profiles are easier to inspect, validate, and generate from an agent.

### A database-backed variant manager

Deferred because it would add infrastructure and reduce portability for a local-first tool.

## Consequences

- The schema and selection rules must be documented clearly.
- The renderer needs deterministic filtering and ordering.
- A profile can be reviewed as a small, auditable change before producing a PDF.
- New templates can reuse the same data and profile model.
