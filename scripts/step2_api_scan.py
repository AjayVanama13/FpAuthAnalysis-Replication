import os, re, json

DECODED_DIR = "../decoded_apks"

# All fingerprint API signatures to search for
FPAPI_PATTERNS = [
    # FingerprintManager (old API, level 23-27)
    "Landroid/hardware/fingerprint/FingerprintManager;->authenticate",
    "Landroid/hardware/fingerprint/FingerprintManager;->isHardwareDetected",
    "Landroid/hardware/fingerprint/FingerprintManager;->hasEnrolledFingerprints",
    # BiometricPrompt (new API, level 28+)
    "Landroid/hardware/biometrics/BiometricPrompt;->authenticate",
    "Landroid/hardware/biometrics/BiometricPrompt$Builder;->build",
    # androidx compat
    "Landroidx/biometric/BiometricPrompt;->authenticate",
    "Landroidx/biometric/BiometricManager;->canAuthenticate",
]

results = []

for app_name in os.listdir(DECODED_DIR):
    app_dir = os.path.join(DECODED_DIR, app_name)
    found_apis = []
    for root, dirs, files in os.walk(app_dir):
        for fname in files:
            if fname.endswith(".smali"):
                path = os.path.join(root, fname)
                with open(path, "r", errors="ignore") as f:
                    content = f.read()
                for pattern in FPAPI_PATTERNS:
                    if pattern in content:
                        found_apis.append(pattern)
    found_apis = list(set(found_apis))
    results.append({"app": app_name, "fpapi_calls": found_apis, "has_fpapi": len(found_apis) > 0})
    print(f"{app_name}: {len(found_apis)} FpAPI calls found")

with open("../results/phase2_api_scan.json", "w") as f:
    json.dump(results, f, indent=2)
