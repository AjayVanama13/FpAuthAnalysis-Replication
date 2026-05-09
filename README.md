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

