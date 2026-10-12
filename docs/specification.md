# ResumeForge Specification

## Objective

ResumeForge is a public, local-first toolkit that helps a job seeker maintain professional information once and generate tailored CV PDFs for different job applications. It must make content changes easy for both humans and AI agents while keeping layout and compilation reproducible through Docker.

The first release targets technically comfortable users who can edit YAML, Markdown, and LaTeX. It must remain approachable enough for an AI agent to explain, validate, and modify the project safely.

## Confirmed requirements

- Repository name: `ResumeForge`.
- Repository visibility: public.
- License: MIT.
- Local path: `~/Documents/Repositories/ResumeForge`.
- Generated CV languages: English and Spanish.
- Generated CV length: between one and three pages.
- Source model: YAML for structured data, Markdown for narrative text, and LaTeX for presentation.
- Initial template count: one professional, extensible template.
- Tailoring model: job-specific profiles plus an optional LLM-generated profile draft from a job description.
- Initial AI integration: documentation and prompts only; no mandatory provider API.
- Future AI integration: design boundaries may support remote or local providers later.
- Build environment: Docker and Docker Compose.
- Local command interface: profile-based commands such as `build --profile <name>`.
- Optional PDF encryption: local environment variable or GitHub Actions secret; secrets must not be committed or logged.
- CI/CD: add only useful validation and artifact generation workflows.
- Reference material: a user-provided reference file can be placed in `reference/`.

## Commands

Planned commands for the first implementation:

```bash
docker compose build
docker compose run --rm resume validate --profile example
docker compose run --rm resume build --profile example
docker compose run --rm resume build --profile example --language en
docker compose run --rm resume build --profile example --language es
docker compose run --rm resume build --all
```

The exact command implementation may be simplified if a Makefile or shell wrapper provides a clearer cross-platform interface, but the profile-based behavior is required.

## Project structure

```text
.data/ or data/             Shared structured content and translations
profiles/                   Job-specific inclusion and prioritization settings
templates/                  LaTeX template and style assets
scripts/                    Validation, rendering, and PDF post-processing helpers
output/                     Generated PDFs and intermediate files; ignored by Git
reference/                  User-provided visual reference documents
docs/                       User guides, prompts, and ADRs
tasks/                      Plan and implementation checklist
.github/workflows/          CI and optional artifact workflows
docker-compose.yml         Reproducible local entry point
Dockerfile                  LaTeX/Python build image definition
```

## Data and rendering model

1. A shared profile contains reusable professional facts and localized text.
2. A job profile selects and prioritizes entries without copying the full shared profile.
3. A renderer validates input and produces an intermediate LaTeX document.
4. XeLaTeX or LuaLaTeX compiles the intermediate document inside Docker.
5. A page-count check rejects output outside the one-to-three-page range.
6. An optional PDF encryption step protects the final file using a secret supplied at runtime.

All user-controlled content must be escaped or inserted through a safe rendering boundary before it reaches LaTeX.

## Code style

- Documentation and source comments are written in English.
- Use small, explicit scripts rather than premature framework abstractions.
- Keep data, selection rules, rendering, and presentation separate.
- Prefer deterministic output and clear validation errors.
- Never place personal secrets or runtime passwords in committed files.

Example profile shape:

```yaml
name: platform-engineer
language: en
summary: platform-engineer-summary.md
include:
  experience:
    - current-role
    - infrastructure-migration
  projects:
    - internal-platform
prioritize:
  skills:
    - Kubernetes
    - Terraform
```

## Testing strategy

The initial project should include:

- Schema and configuration validation tests.
- Rendering tests for English and Spanish sample data.
- A build smoke test that confirms a PDF is produced.
- A page-count test enforcing the one-to-three-page requirement.
- A negative test proving invalid profiles fail before compilation.
- CI validation for the example profile and template.

The first CI workflow should avoid publishing real personal data. It may publish a synthetic example PDF as an artifact if that adds value.

## Security boundaries

### Always do

- Treat YAML, Markdown, profile files, and job descriptions as untrusted input.
- Escape LaTeX-sensitive characters at the rendering boundary.
- Keep passwords in environment variables or GitHub Actions secrets.
- Mask secrets and avoid printing command lines that contain them.
- Ignore generated output and local secret files by default.
- Run dependency and container checks where practical.

### Ask first

- Adding a provider-specific LLM integration.
- Uploading personal source data to an external service.
- Publishing a real CV through GitHub Pages or a public release.
- Changing the encryption model or secret handling.
- Adding a frontend that accepts or stores credentials.

### Never do

- Commit API keys, passwords, tokens, or private keys.
- Put a PDF password in YAML, Markdown, workflow source, or command output.
- Treat PDF encryption as a replacement for repository access controls.
- Execute arbitrary LaTeX or shell content generated by an LLM without validation.
- Disable failed validation merely to produce a PDF.

## Success criteria

- A fresh clone can build the synthetic example PDF with Docker Compose and no host LaTeX installation.
- The same data can produce English and Spanish PDFs.
- A job-specific profile can include, exclude, and prioritize reusable content.
- The build fails clearly when input is invalid or output exceeds three pages.
- The optional encryption path works locally without exposing the password.
- CI validates the repository and produces a synthetic artifact without requiring personal secrets.
- Documentation explains setup, data modeling, profile creation, agent prompts, troubleshooting, and contribution.
- A user-provided reference document can be used to refine the template without becoming a required build input.

## Open questions

- The visual design and exact page geometry will be finalized after the reference PDF is added.
- The final LaTeX engine and base image will be selected after testing font and multilingual support.
- GitHub Pages will be considered for documentation or synthetic examples, not assumed for private CV delivery.
