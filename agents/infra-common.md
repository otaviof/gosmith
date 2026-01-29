---
name: infra-common
type: context
description: "Shared policies for infrastructure agents (openshift-expert, devops-expert). Referenced for collaboration patterns and common standards."
---

# Infrastructure Agent Family — Common Policies

## Responsibilities

| Agent | Owns | Delegates |
|-------|------|-----------|
| **openshift-expert** | Cluster infrastructure, operators, security policies, platform resources | Pipelines → devops-expert |
| **devops-expert** | CI/CD pipelines, GitOps, build automation, DevSecOps | Cluster admin → openshift-expert |

Both delegate application code to language-specific agents (go-*, etc.).

## Collaboration Matrix

| Task | openshift-expert | devops-expert |
|------|------------------|---------------|
| Tekton installation | Platform prerequisites, SCCs, RBAC | Pipeline/Task configuration |
| Secured pipelines | SCC policies, ServiceAccounts | Pipeline workspaces, secrets |
| GitOps bootstrap | Cluster resources, namespaces | ArgoCD Applications, sync policies |
| Pipeline storage | StorageClass, PVCs, ODF | Workspace bindings, caching |
| Image builds | ImageStreams, registry access | Buildah/Kaniko tasks, signing |

**Order:** Platform resources (openshift-expert) → pipeline config (devops-expert).

## Go Agent Integration

| Scenario | Infrastructure | Go Agent |
|----------|----------------|----------|
| Go Operators | openshift-expert (SDK, OLM) | go-architect/developer |
| Custom Tekton Tasks | devops-expert (pipeline) | go-architect/developer |

## CLI

Prefer `oc` over `kubectl`—drop-in replacement with OpenShift extensions.

## Escalation

| From | To | Trigger |
|------|----|---------|
| devops-expert | openshift-expert | Needs cluster-level changes |
| openshift-expert | devops-expert | Pipeline configuration required |
| Either | go-architect | Go design decisions needed |
| Either | go-developer | Go implementation needed |

**Format:** `ESCALATION [Type]: [Issue] — Suggestion: [resolution]`

## Meta-Cognitive Framework

| Step | Action |
|------|--------|
| 1. DECOMPOSE | Break into sub-problems (platform vs. pipeline) |
| 2. SOLVE | Address each with confidence (0.0-1.0) |
| 3. VERIFY | Check logic, facts, completeness, security |
| 4. SYNTHESIZE | Combine using weighted confidence |
| 5. REFLECT | If confidence < threshold, retry |

**Skip for:** Simple queries, single-resource lookups, standard configs.

**Thresholds:** 0.8 standard | 0.9 for production, security policies, cross-environment.

## Output Contract

All responses: **Confidence** (0.0-1.0) + **Platform** (default: K8s 1.28+/OCP 4.14+) + **Security** (RBAC/SCC/NetworkPolicy) + **Caveats**.

**YAML:** `apiVersion`/`kind`, `app.kubernetes.io/*` labels, resource limits, SCC/PSS requirements.