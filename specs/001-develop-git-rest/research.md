# Phase 0 Research: git-rest Implementation

## Research Tasks

1. **Research target concurrency and load requirements for a Flask-based git-backed REST API**
   - What is a reasonable default for concurrent users and requests per second for a content management backend using Flask, Gunicorn, and gitpython?
   - What are the performance bottlenecks when using gitpython for repository operations in a multi-user environment?

2. **Research multi-tenant vs. single-tenant requirements for git-rest**
   - What are the best practices for supporting multiple users or organizations in a file-system-based, git-backed backend?
   - What are the security and isolation concerns if multiple users access the same backend instance?

3. **Research expected repository size and usage patterns**
   - What are the practical limits for repository size and number of files when using gitpython in a server context?
   - How do large repositories impact API response times and server resource usage?

## Consolidated Findings

<!--
For each research task, fill in:
- Decision: [what was chosen]
- Rationale: [why chosen]
- Alternatives considered: [what else evaluated]
-->

### 1. Target Concurrency and Load
 Decision: Target support for up to 100 concurrent users, with typical usage patterns reflecting a team of up to 100 people, each using the application no more than 60% of the workday.
 Rationale: The application is intended for internal team use in a development environment, not for public internet-scale workloads. Flask with Gunicorn (using 4-8 workers) and proper reverse proxying (Nginx) is sufficient for this scale. Git operations are typically I/O bound and not constant, so this concurrency is reasonable.
 Alternatives considered: Higher concurrency (1000+ users) would require async frameworks or horizontal scaling; for this use case, Flask + Gunicorn is appropriate.

### 2. Multi-Tenant vs. Single-Tenant
 Decision: Support for multiple repositories per backend instance, with each repository logically isolated. Multi-user access is allowed, but all users are assumed to be trusted team members (no strict tenant isolation).
 Rationale: The "do one thing and do it well" philosophy and good multi-repo practices mean each repo is managed independently. Security is handled at the infrastructure level (network, authentication, etc.), not within the app.
 Alternatives considered: Full multi-tenant isolation (per-user sandboxes) is not required for this team use case; could be added in future if needed.

### 3. Repository Size and Usage
 Decision: Target small to medium repositories (up to ~1GB, <100k files per repo). Large monorepos are discouraged; encourage modular repo design.
 Rationale: Team development best practices favor smaller, focused repositories. gitpython and the file system can efficiently handle this scale. For larger repos, performance may degrade and would require architectural changes.
 Alternatives considered: Supporting very large repos (10GB+, millions of files) would require a different backend or sharding approach.
