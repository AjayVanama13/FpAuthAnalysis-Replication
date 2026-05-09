import os, json

DECODED_DIR = "../decoded_apks"

DEACTIVATE_KEYWORDS = [
    "disableBiometric", "removeFingerprintAuth", "setFingerprintEnabled",
    "biometric_disable", "fingerprint_off", "disableFingerprint"
]
AUTH_KEYWORDS = ["checkPassword", "verifyPin", "authenticate", "checkCredential"]

results = []
for app_name in os.listdir(DECODED_DIR):
    app_dir = os.path.join(DECODED_DIR, app_name)
    deactivate_found = False
    auth_near_deactivate = False

    for root, dirs, files in os.walk(app_dir):
        for fname in files:
            if not fname.endswith(".smali"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", errors="ignore") as f:
                content = f.read()
                lines = content.split("\n")
            for i, line in enumerate(lines):
                if any(k.lower() in line.lower() for k in DEACTIVATE_KEYWORDS):
                    deactivate_found = True
                    context = "\n".join(lines[max(0,i-20):i+20])
                    if any(k.lower() in context.lower() for k in AUTH_KEYWORDS):
                        auth_near_deactivate = True

    misuse = deactivate_found and not auth_near_deactivate
    results.append({"app": app_name, "misuse_type3_unauthorized_deactivation": misuse})
    print(f"{app_name}: Unauthorized Deactivation = {misuse}")

with open("../results/misuse_type3.json", "w") as f:
    json.dump(results, f, indent=2)
