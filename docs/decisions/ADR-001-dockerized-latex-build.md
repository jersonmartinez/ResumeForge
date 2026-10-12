# ADR-001: Use a Dockerized LaTeX build environment

## Status

Accepted

## Context

ResumeForge must generate reproducible PDFs for users on Windows, macOS, and Linux without requiring each user to install and maintain a local LaTeX distribution. LaTeX packages, fonts, and auxiliary tools must be consistent between local builds and GitHub Actions.

## Decision

Use Docker and Docker Compose as the primary build interface. The repository will provide a versioned build image containing the required rendering and validation tools. Generated files will be mounted to a local output directory.

## Alternatives considered

### Host-installed LaTeX

Rejected for the default workflow because installation and package management differ significantly across operating systems.

### GitHub Actions only

Rejected because users need a reliable local workflow for private or iterative CV generation.

### A hosted web application

Deferred. A hosted application would introduce data privacy, authentication, storage, and operational requirements that are not necessary for the first release.

## Consequences

- Users need Docker Desktop or an equivalent Docker installation.
- Builds are more reproducible across environments.
- The image may be large because multilingual LaTeX support requires a substantial package set.
- CI can run the same containerized build used locally.
