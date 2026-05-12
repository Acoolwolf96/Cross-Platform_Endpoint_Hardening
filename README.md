# Cross-Platform Endpoint Hardening Agent with Policy-as-Code

A lightweight, modular, and intelligent security agent for Windows, Linux, and macOS endpoints that enforces system hardening based on CIS/NIST/custom benchmarks. It supports YAML/JSON-based declarative policies, real-time drift detection, auto-remediation, and cloud-native visibility.

\---

## Overview

Modern cyber threats often exploit misconfigurations, default settings, or deviations from security baselines. This agent ensures system configurations remain continuously aligned with desired security states, reducing the attack surface and supporting regulatory compliance.

This project represents a **security-as-code** paradigm, unifying **compliance**, **hardening**, and **response** into a programmable and auditable endpoint agent.

\---

## Key Features

### Cross-Platform Support

* **Windows**, **Linux**, and **macOS**
* Abstracted OS-specific operations via a pluggable backend system
* Designed in **C++ (core)** and **Python (policy layer/agent orchestration)**

### Policy-as-Code (PaC)

* Declarative policies defined in **YAML** or **JSON**
* Schema validation for integrity and consistency
* Supports CIS Benchmarks, NIST 800-53, ISO 27001, and custom controls
* Policies define:

  * `check`: how to validate the current state
  * `desired\_state`: what the system should look like
  * `remediate`: instructions to fix non-compliance

### Intelligence \& Adaptability

* **Drift Detection**: Monitors system configurations for deviation from the defined policy
* **Auto-Remediation**: Reverts unauthorized or accidental changes to system settings
* **Context-Aware Enforcement**:

  * Detects runtime context (OS, version, role)
  * Applies relevant subset of policies dynamically
* **Change Audit**: Logs policy violations and remediations for full traceability

### Cloud Dashboard Integration (Planned)

* Centralized view of policy compliance across fleet
* Real-time metrics, alerts, and historical trends
* API for SIEM/SOAR integration

### Secure by Design

* Runs with least privileges required
* Agent integrity checks with optional signature verification
* Logs signed with hash chains to prevent tampering

\---

## Why This Matters

### Problem

Security configuration drift, unpatched settings, and inconsistent hardening are common root causes of breaches. Traditional agents are:

* Opaque and proprietary
* Hard to customize
* Inflexible across platforms

### Solution Intelligence

This project embeds a **lightweight reasoning engine** with:

* Declarative configuration logic
* Real-time validation
* Adaptive remediation
* Minimal overhead

This enables **automated enforcement at scale**, aligned with **DevSecOps**, **zero-trust**, and **compliance-as-code** philosophies.

\---

## Example Policy

```yaml
id: cis\_ubuntu\_1\_1\_1
title: "Ensure mounting of cramfs filesystems is disabled"
description: "Disabling cramfs reduces attack surface"
platforms: \["linux"]
severity: "high"
check: "modprobe -n -v cramfs | grep -q 'install /bin/true'"
desired\_state: "modprobe --install cramfs /bin/true"
remediate: |
  echo 'install cramfs /bin/true' >> /etc/modprobe.d/cramfs.conf
```

\---

## Use Cases

* **Enterprise Security Teams**:

  * Continuous hardening aligned with benchmarks
  * Reduce manual compliance overhead
* **MSSPs / MDR Providers**:

  * Policy-as-a-service across multi-tenant environments
  * Centralized control with local enforcement
* **DevSecOps Pipelines**:

  * Integrate compliance checks in CI/CD
  * Bake hardened images automatically
* **Critical Infrastructure \& Air-Gapped Environments**:

  * Local-first enforcement, no reliance on cloud
  * Offline logging and audit trails

\---

## Getting Started

### Installation

```bash
git clone https://github.com/your-org/endpoint-hardening-agent.git
cd endpoint-hardening-agent
pip install -r requirements.txt
make build
```

### Run Agent

```bash
python agent.py --policy policies/cis-ubuntu.yaml
```

Or as a daemon:

```bash
sudo systemctl enable hardening-agent
sudo systemctl start hardening-agent
```

\---

## Security Considerations

* Agent and its configuration should be deployed via trusted channels
* All remediation actions are logged
* Future enhancement: allow signed and verified policies

\---

## Project Intelligence Summary

* **Why**: Endpoint misconfigurations are low-hanging fruit for attackers. Hardening is vital but difficult to maintain at scale.
* **How**:

  * Declarative PaC reduces complexity
  * Real-time detection + self-healing boosts resilience
  * Cross-platform design supports heterogeneous fleets
* **What makes it intelligent**:

  * Dynamic OS-role-context aware decisions
  * Continuous drift reconciliation
  * Future extensibility via machine learning anomaly detection on config drifts

\---

