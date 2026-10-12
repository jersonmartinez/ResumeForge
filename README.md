# ResumeForge

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-required-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![LaTeX](https://img.shields.io/badge/LaTeX-reproducible-008080?logo=latex&logoColor=white)](https://www.latex-project.org/)
[![CI](https://github.com/jersonmartinez/ResumeForge/actions/workflows/ci.yml/badge.svg)](https://github.com/jersonmartinez/ResumeForge/actions/workflows/ci.yml)

ResumeForge is a Dockerized, open-source toolkit for maintaining one professional profile and generating tailored CV versions for different job applications.

The project separates content from presentation:

- YAML stores structured professional data.
- Markdown stores longer narrative content.
- LaTeX controls layout and typography.
- Docker Compose provides a reproducible build environment.
- Job-specific profiles select, prioritize, and customize content.
- Agent instructions help an AI assistant create or review tailored profiles without requiring a provider-specific API integration.

> Project status: initial foundation. The reference directory is intentionally empty so a visual reference PDF can be added before the first template is finalized.

## Planned quick start

```bash
docker compose run --rm resume validate --profile example
docker compose run --rm resume build --profile example
```

Generated files will be written to `output/` and will not be committed by default.

## Repository layout

```text
ResumeForge/
├── .github/workflows/       # Automated validation and build workflows
├── data/                    # Shared resume data and language content
├── docs/                    # User documentation and architecture decisions
├── profiles/                # Job-specific configurations
├── reference/               # Optional visual reference documents
├── scripts/                 # Validation and rendering helpers
├── templates/               # LaTeX templates
├── tasks/                   # Project plan and implementation checklist
├── docker-compose.yml       # Local build entry point
└── LICENSE
```

## Privacy and published PDFs

ResumeForge can optionally encrypt generated PDFs. Passwords must be supplied through a local environment variable or a GitHub Actions secret; they must never be committed to the repository or printed in workflow logs.

A public repository is not a privacy boundary. Anyone with access to public source data can reconstruct an unencrypted CV. Use a private repository or keep sensitive source files outside version control when confidentiality is required.

## Documentation

The implementation specification is in [`docs/specification.md`](docs/specification.md). Architecture decisions are recorded in [`docs/decisions/`](docs/decisions/), and the implementation plan is in [`tasks/plan.md`](tasks/plan.md).

## License

ResumeForge is distributed under the MIT License. See [`LICENSE`](LICENSE).
