import json, pandas as pd

# Load all misuse results
with open("../results/phase2_api_scan.json") as f:
    api_data = {d["app"]: d for d in json.load(f)}
with open("../results/misuse_type1.json") as f:
    m1 = {d["app"]: d for d in json.load(f)}
with open("../results/misuse_type2.json") as f:
    m2 = {d["app"]: d for d in json.load(f)}
with open("../results/misuse_type3.json") as f:
    m3 = {d["app"]: d for d in json.load(f)}
with open("../results/misuse_type4.json") as f:
    m4 = {d["app"]: d for d in json.load(f)}

rows = []
for app in api_data:
    if not api_data[app]["has_fpapi"]:
        continue
    t1 = m1.get(app, {}).get("misuse_type1_obsolete_api", False)
    t2 = m2.get(app, {}).get("misuse_type2_no_crypto", False)
    t3 = m3.get(app, {}).get("misuse_type3_unauthorized_deactivation", False)
    t4 = m4.get(app, {}).get("misuse_type4_fp_update_ignored", False)
    count = sum([t1, t2, t3, t4])
    rows.append({
        "App": app,
        "Obsolete API": "✓" if t1 else "✗",
        "No Crypto Binding": "✓" if t2 else "✗",
        "Unauthorized Deactivation": "✓" if t3 else "✗",
        "FP Update Ignored": "✓" if t4 else "✗",
        "Total Misuses": count,
        "Vulnerable": count > 0
    })

df = pd.DataFrame(rows)
print(df.to_string())
print(f"\nTotal apps analyzed: {len(df)}")
print(f"Apps with ≥1 misuse: {df['Vulnerable'].sum()} ({100*df['Vulnerable'].mean():.1f}%)")
print(f"Apps with all 4 misuses: {(df['Total Misuses']==4).sum()}")

df.to_csv("../results/final_results.csv", index=False)
print("\nSaved to results/final_results.csv")
