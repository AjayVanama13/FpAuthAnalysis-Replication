import os
import subprocess
import xml.etree.ElementTree as ET

APK_DIR = "apks"
DECODED_DIR = "../decoded_apks"
FP_PERMISSIONS = {"android.permission.USE_BIOMETRIC", "android.permission.USE_FINGERPRINT"}

results = []

for apk_name in os.listdir(DECODED_DIR):
    manifest_path = os.path.join(DECODED_DIR, apk_name, "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        continue
    tree = ET.parse(manifest_path)
    root = tree.getroot()
    ns = "http://schemas.android.com/apk/res/android"
    permissions = {elem.get(f"{{{ns}}}name") for elem in root.findall(".//uses-permission")}
    has_fp_perm = bool(permissions & FP_PERMISSIONS)
    results.append({"app": apk_name, "has_fp_permission": has_fp_perm})
    print(f"{apk_name}: {'✓ FP permission' if has_fp_perm else '✗ no FP permission'}")

# Save
import json
with open("../results/phase1_permission_filter.json", "w") as f:
    json.dump(results, f, indent=2)
