import json, os

with open("../results/phase2_api_scan.json") as f:
    api_data = json.load(f)

OLD_API = "Landroid/hardware/fingerprint/FingerprintManager;->authenticate"
NEW_API_PATTERNS = [
    "Landroid/hardware/biometrics/BiometricPrompt",
    "Landroidx/biometric/BiometricPrompt"
]

results = []
for app in api_data:
    if not app["has_fpapi"]:
        continue
    uses_old = any(OLD_API in c for c in app["fpapi_calls"])
    uses_new = any(any(n in c for n in NEW_API_PATTERNS) for c in app["fpapi_calls"])
    misuse = uses_old and not uses_new   # exclusively old API
    results.append({
        "app": app["app"],
        "misuse_type1_obsolete_api": misuse,
        "uses_old_api": uses_old,
        "uses_new_api": uses_new
    })
    print(f"{app['app']}: Obsolete API misuse = {misuse}")

with open("../results/misuse_type1.json", "w") as f:
    json.dump(results, f, indent=2)
