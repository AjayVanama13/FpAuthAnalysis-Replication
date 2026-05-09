import os, json

DECODED_DIR = "../decoded_apks"

results = []
for app_name in os.listdir(DECODED_DIR):
    app_dir = os.path.join(DECODED_DIR, app_name)
    explicitly_false = False
    key_builder_found = False

    for root, dirs, files in os.walk(app_dir):
        for fname in files:
            if not fname.endswith(".smali"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", errors="ignore") as f:
                lines = f.readlines()
            for i, line in enumerate(lines):
                if "setInvalidatedByBiometricEnrollment" in line:
                    key_builder_found = True
                    # Check if the preceding constant is 0 (false)
                    if i > 0 and ("0x0" in lines[i-1] or "false" in lines[i-1].lower()):
                        explicitly_false = True
                if "KeyGenParameterSpec" in line or "setUserAuthenticationRequired" in line:
                    key_builder_found = True

    # If key builder found but invalidation not set = defaults to true (safe)
    # If explicitly set to false = misuse
    misuse = explicitly_false
    results.append({
        "app": app_name,
        "misuse_type4_fp_update_ignored": misuse,
        "key_builder_found": key_builder_found
    })
    print(f"{app_name}: Mishandled FP Updates = {misuse}")

with open("../results/misuse_type4.json", "w") as f:
    json.dump(results, f, indent=2)
