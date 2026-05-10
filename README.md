# FpAuthAnalysis Replication

Replication of the NDSS research paper:

"An Empirical Study on Fingerprint API Misuse with Lifecycle Analysis in Real-world Android Apps"

## Objective
Detect insecure fingerprint authentication implementations in Android applications using static analysis.

## Features
- APK decompilation
- Manifest permission analysis
- Fingerprint API detection
- Lifecycle misuse detection
- Callback misuse analysis
- CryptoObject validation

## Technologies Used
- Python
- APKTool
- JADX
- FlowDroid
- Androguard

## Workflow
APK → Decompiled APK → Static Analysis → Misuse Detection → Result Aggregation

## Setup
- Java 11
- Python 3.12
- Android SDK
- FlowDroid 2.10

Dataset Used
The project analyzes Android applications implementing biometric authentication.

Sample applications analyzed:
- Dashlane
- Bitwarden
- KeePassDX
- Aegis Authenticator
- Standard Notes
- AppLock

The original NDSS paper analyzed more than 1300 applications.
This replication uses a lightweight curated dataset of 20–30 APKs.

Novelty Work
This project introduces a lightweight and modular replication of the original NDSS workflow.

Key contributions:
- Lightweight replication using a small curated APK dataset
- Modular misuse detection scripts
- Static-only analysis without runtime instrumentation
- WSL Ubuntu based reproducible research workflow
- Simplified educational implementation of Android biometric security analysis

How It Works
1. APK files are collected from APKMirror, APKPure, and F-Droid.
2. APKs are decompiled using APKTool.
3. AndroidManifest.xml is analyzed for biometric permissions.
4. Decompiled code is scanned for fingerprint APIs.
5. Lifecycle methods are analyzed for authentication cancellation handling.
6. Authentication callbacks are inspected.
7. CryptoObject validation is checked.
8. Results are aggregated into structured reports.

Project Structure
```text
FpAuthAnalysis/
│
├── scripts/
├── results/
├── apks/
├── decoded_apks/
├── README.md
├── requirements.txt
└── CNS_PROJECT_REPORT.pdf
