---
name: cicd-common
type: context
description: "Shared DevSecOps, secrets management, and container build standards for CI/CD agents (tekton-expert, gha-expert)."
---

# CI/CD Agent Family — Common Policies

Platform-agnostic standards referenced by [tekton-expert](tekton-expert.md) and [gha-expert](gha-expert.md).

## DevSecOps

### SLSA Compliance

| Level | Requirements |
|-------|--------------|
| SLSA 1 | Build process documented, provenance generated |
| SLSA 2 | Hosted build service, signed provenance |
| SLSA 3 | Hardened build platform, non-falsifiable provenance |

Target SLSA 2+ for production artifacts.

### SBOM Generation

Generate Software Bill of Materials for all container images:

| Format | Use Case |
|--------|----------|
| CycloneDX | Preferred for vulnerability scanning integration |
| SPDX | Compliance-focused, license analysis |

Attach SBOM as image attestation or store alongside artifacts.

### Vulnerability Scanning

Integrate scanning early in the pipeline (shift-left):

| Stage | Scan Type |
|-------|-----------|
| Build | Dependency vulnerabilities (Trivy, Snyk, Grype) |
| Build | Static analysis (SonarQube, CodeQL, Semgrep) |
| Post-build | Container image scanning |
| Runtime | Continuous monitoring (optional) |

Fail builds on critical/high vulnerabilities. Allow documented exceptions.

### Artifact Signing

Sign all production artifacts:

| Tool | Purpose |
|------|---------|
| Cosign/Sigstore | Keyless signing with OIDC identity |
| Notation | OCI-native signing |

Verify signatures before deployment.

## Secrets Management

### Principles

| Principle | Rule |
|-----------|------|
| Never hardcode | No secrets in code, configs, or logs |
| Least privilege | Minimal permissions, job-scoped |
| Prefer OIDC | Workload identity over static credentials |
| Rotate regularly | Automate rotation where possible |
| Audit access | Log access for compliance |

### OIDC over Static Secrets

| Platform | OIDC Provider |
|----------|---------------|
| GitHub Actions | GitHub OIDC → AWS/GCP/Azure |
| Tekton | Kubernetes ServiceAccount → cloud IAM |

OIDC eliminates long-lived credentials. Configure trust policies to restrict access by repository, branch, or environment.

### Secret Injection

| Approach | When to Use |
|----------|-------------|
| Environment variables | Simple cases, single values |
| Mounted files | Certificates, config files |
| External secrets operator | Kubernetes, dynamic rotation |

Never log secret values. Use masking where available.

## Container Builds

### Multi-Stage Patterns

```dockerfile
# Build stage - includes tools
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN go build -o /app/binary

# Runtime stage - minimal
FROM gcr.io/distroless/static
COPY --from=builder /app/binary /
ENTRYPOINT ["/binary"]
```

Separate build dependencies from runtime image.

### Layer Optimization

| Practice | Benefit |
|----------|---------|
| Order by change frequency | Cache hits |
| Combine RUN commands | Fewer layers |
| Use `.dockerignore` | Smaller context |
| Pin base image digests | Reproducibility |

### Base Image Selection

| Type | Use Case |
|------|----------|
| Distroless | Production, minimal attack surface |
| Alpine | Small size, includes shell for debugging |
| Scratch | Static binaries only |
| UBI (Red Hat) | OpenShift, RHEL compliance |

Prefer minimal images. Scan base images for vulnerabilities.

### Caching Strategies

| Platform | Approach |
|----------|----------|
| GitHub Actions | `actions/cache`, Docker layer caching |
| Tekton | Workspace persistence, Buildah layer cache |

Cache dependencies separately from source code for optimal reuse.