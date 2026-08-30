# 🛡️ Security Policy & Biometric Privacy

## Supported Versions

Security updates and patches are applied to the latest release of HARIS.

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

---

## 🔒 Biometric Privacy & Data Handling

HARIS is architected around **privacy-first principles**:

1. **On-Device Storage**: All captured facial images (`data/<username>/`) and trained model weights (`data/classifiers/`) are stored strictly on the local filesystem. No biometric telemetry or video feeds are transmitted over external networks.
2. **Exclusion from Version Control**: When publishing or sharing modifications, do not commit raw facial image folders to public version control.
3. **QR Token Security**: Photo-embedded QR passes encode structured identification strings. For high-security environments, payloads can be configured with HMAC or asymmetric digital signatures.

---

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability or security bug within HARIS:

1. **Do not** report security vulnerabilities via public GitHub issues.
2. Please contact the maintainer directly via GitHub or email: **Sameer Abbas**.
3. Include detailed steps to reproduce the vulnerability, along with potential mitigations if available.
4. The maintainer will acknowledge receipt within 48 hours and work on a resolution.
