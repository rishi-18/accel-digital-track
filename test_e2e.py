import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

BASE = "http://localhost:3000/api/v1"

def test_e2e():
    print("--- 1. Testing Catalog Recommendation ---")
    rec_res = requests.post(f"{BASE}/catalog/recommend", json={
        "business_type": "Kirana / Retail",
        "employee_count": 3,
        "num_sites": 1,
        "has_gstin": True,
        "city_tier": 1,
        "budget_inr": 2000,
        "requires_calling_sims": True,
        "preferred_language": "en"
    })
    assert rec_res.status_code == 200
    bundles = rec_res.json()["bundles"]
    print(f"Generated {len(bundles)} bundles. Selected: {bundles[0]['title']} (₹{bundles[0]['total_mrc']}/mo)")

    print("\n--- 2. Testing K01 Defect Interception (Vindhya Tours) ---")
    k01_res = requests.post(f"{BASE}/kyc/verify-dossier", data={
        "applicant_id": "APP-K01",
        "gstin": "37IHKXV5167L1ZS",
        "udyam_no": "", # Missing Udyam defect
        "signatory_name": "Neha Kaur",
        "pincode": "118383", # Mismatched northern pincode for AP defect
        "dpdp_consent": "true"
    })
    assert k01_res.status_code == 200
    k01_data = k01_res.json()
    print("K01 Verdict:", k01_data["verification_verdict"])
    print("K01 Flags:", k01_data["security_flags"])
    assert k01_data["verification_verdict"] == "ASSISTED_REVIEW"

    print("\n--- 3. Testing K02 Syntax Rejection (Harmony Dental) ---")
    k02_res = requests.post(f"{BASE}/kyc/verify-dossier", data={
        "applicant_id": "APP-K02",
        "gstin": "19E0GXH4115Y1ZL", # Planted malformed '0' in PAN
        "udyam_no": "UDYAM-WB-00-5053330",
        "signatory_name": "Joseph Shah",
        "pincode": "347550",
        "dpdp_consent": "true"
    })
    assert k02_res.status_code == 200
    k02_data = k02_res.json()
    print("K02 Verdict:", k02_data["verification_verdict"])
    print("K02 Flags:", k02_data["security_flags"])
    assert k02_data["verification_verdict"] == "REJECTED"

    print("\n--- 4. Testing K03 Auto-Approval (Ganesh Woodcraft) ---")
    k03_res = requests.post(f"{BASE}/kyc/verify-dossier", data={
        "applicant_id": "APP-K03",
        "gstin": "27XUIXG0767D1ZP",
        "udyam_no": "UDYAM-MH-00-9516696",
        "signatory_name": "Joseph Singh",
        "pincode": "411231",
        "dpdp_consent": "true"
    })
    assert k03_res.status_code == 200
    k03_data = k03_res.json()
    print("K03 Verdict:", k03_data["verification_verdict"])
    assert k03_data["verification_verdict"] == "AUTO_APPROVED"

    print("\n--- 5. Testing Order Creation & Cryptographic Tracking ---")
    order_res = requests.post(f"{BASE}/order/create", json={
        "applicant_id": "APP-K03",
        "bundle_id": "office-pro",
        "bundle_name": "Office Pro Connect",
        "monthly_mrc": 2498,
        "one_time_setup": 0,
        "contract_months": 12,
        "selected_addons": ["Static Public IP"],
        "business_name": "Ganesh Woodcraft",
        "signatory_name": "Joseph Singh",
        "contact_phone": "9811234567",
        "delivery_pincode": "411231",
        "signed_kyc_token": k03_data["signed_token"],
        "verification_verdict": k03_data["verification_verdict"]
    })
    assert order_res.status_code == 200
    order = order_res.json()
    print("Created Order:", order["order_id"])
    print("HMAC Signature:", order["hmac_signature"][:16] + "...")
    print("Technician:", order["technician"]["name"], "(Slot:", order["technician"]["slot"], ")")

    print("\n--- 6. Testing Partner Desk Drop-Off Queue & Action Dispatch ---")
    queue_res = requests.get(f"{BASE}/analytics/propensity-queue?limit=5")
    assert queue_res.status_code == 200
    top_lead = queue_res.json()[0]
    print(f"Top Recoverable Lead: {top_lead['business_name']} (Score: {top_lead['propensity_score']}, Priority: {top_lead['priority']})")
    print(f"Score Breakdown: {top_lead['score_breakdown']}")

    action_res = requests.post(f"{BASE}/partner/action", json={
        "action_type": "DISPATCH_WHATSAPP_KYC",
        "lead_id": top_lead["lead_id"],
        "business_name": top_lead["business_name"]
    })
    assert action_res.status_code == 200
    print("Action Dispatch Result:", action_res.json()["message"])

    print("\n>>> ALL 6 END-TO-END VALIDATION TESTS PASSED PERFECTLY! <<<")

if __name__ == "__main__":
    test_e2e()
