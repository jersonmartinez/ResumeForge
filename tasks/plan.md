# Implementation Plan: ResumeForge

## Overview

Build a local-first CV generation toolkit that renders bilingual, job-specific PDFs from shared YAML data, Markdown content, and an extensible LaTeX template. Docker Compose is the primary interface so local builds and CI use the same environment.

## Architecture decisions

- Dockerized LaTeX build environment: see ADR-001.
- Profile-driven variants: see ADR-002.
- Start with one professional template and a stable data contract.
- Use synthetic example data for automated builds.
- Keep PDF encryption optional and secret-driven.
- Treat GitHub Pages as documentation or synthetic-example hosting unless a privacy-preserving delivery model is explicitly added.

## Task list

### Phase 1: Foundation

- [x] Define the data schema for shared content, localized strings, and job profiles.
- [x] Select the initial LaTeX engine and verify the multilingual package direction from the reference documents.
- [x] Add the Docker Compose command surface and a minimal container entrypoint.
- [x] Add synthetic English and Spanish example data following the reference content model.

### Checkpoint: Foundation

- [x] Docker image builds successfully.
- [x] The example configuration validates.
- [x] The repository has no required personal data.

### Phase 2: Rendering

- [x] Implement safe YAML/Markdown loading and LaTeX escaping.
- [x] Implement profile filtering and deterministic ordering.
- [x] Implement the first professional LaTeX template.
- [x] Compile English and Spanish PDFs.
- [x] Enforce the one-to-three-page requirement.

### Checkpoint: Rendering

- [x] Both language variants compile locally through Docker Compose.
- [x] Invalid configuration fails before compilation.
- [x] Generated files are written to the documented output location.

### Phase 3: Delivery and automation

- [x] Add optional PDF encryption using a runtime-provided password.
- [x] Add local and CI documentation for secrets and artifact handling.
- [x] Add GitHub Actions validation and synthetic PDF artifact generation.
- [ ] Add agent prompts for creating and reviewing job profiles.
- [ ] Document how to add a new template.

### Checkpoint: Complete

- [ ] Full validation suite passes.
- [ ] CI builds the synthetic example without personal secrets.
- [ ] README and troubleshooting documentation are complete.
- [x] Reference PDF and DOCX analysis is incorporated into the initial layout and data model.

## Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Multilingual LaTeX package or font incompatibility | High | Test XeLaTeX/LuaLaTeX early with English and Spanish fixtures |
| User content breaks LaTeX compilation | High | Validate and escape all dynamic text before rendering |
| Template exceeds three pages | Medium | Add page-count validation and document density controls |
| Docker image is slow or very large | Medium | Start with a reliable image; optimize only after measuring |
| Password leaks in CI logs or artifacts | High | Use GitHub Secrets, masked variables, and no secret echoing |
| Public source exposes personal data | High | Document the boundary clearly and support private/local source files |

## Open questions

- Exact visual design after the reference file is supplied.
- Whether the final workflow should publish a release asset, an Actions artifact, or both.
- Whether the optional frontend should remain a future phase or become a later companion project.
