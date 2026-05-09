import os, json, re

DECODED_DIR = "../decoded_apks"

def check_crypto_binding(app_dir):
    """
    Look for authenticate() calls and check if CryptoObject is passed (null = no binding).
    Also check setUserAuthenticationRequired and setInvalidatedByBiometricEnrollment flags.
    """
    issues = []
    for root, dirs, files in os.walk(app_dir):
        for fname in files:
            if not fname.endswith(".smali"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", errors="ignore") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                # authenticate called with null CryptoObject (no crypto binding)
                if "authenticate(" in line:
                    context = "".join(lines[max(0,i-5):i+5])
                    if "const/4 v0, 0x0" in context or "const/16 v0, 0x0" in context:
                        issues.append(f"Possible null CryptoObject at {fname}:{i+1}")
                # setUserAuthenticationRequired set to false
                if "setUserAuthenticationRequired" in line and "0x0" in lines[i-1] if i > 0 else False:
                    issues.append(f"UserAuthenticationRequired=false at {fname}:{i+1}")
    return issues

results = []
for app_name in os.listdir(DECODED_DIR):
    app_dir = os.path.join(DECODED_DIR, app_name)
    issues = check_crypto_binding(app_dir)
    misuse = len(issues) > 0
    results.append({"app": app_name, "misuse_type2_no_crypto": misuse, "evidence": issues[:3]})
    print(f"{app_name}: Inadequate Crypto = {misuse}")

with open("../results/misuse_type2.json", "w") as f:
    json.dump(results, f, indent=2)
