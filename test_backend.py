import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    print("Health:", data)
    assert data["dpdp_compliant"] is True

def test_k01():
    # K01: Neha Kaur / Vindhya Tours
    res = client.post("/api/v1/kyc/verify-dossier", data={
        "applicant_id": "APP-K01",
        "gstin": "37IHKXV5167L1ZS",
        "udyam_no": "",
        "signatory_name": "Neha Kaur",
        "pincode": "118383",
        "dpdp_consent": "true"
    })
    print("K01 response:", res.status_code, res.json())
    assert res.status_code == 200
    # K01 has status Cancelled (CRITICAL) or Udyam missing/pincode flag
    assert res.json()["verification_verdict"] in ["ASSISTED_REVIEW", "REJECTED"]

def test_k02():
    # K02: Joseph Shah / Harmony Dental (Malformed GSTIN with 19E0...)
    res = client.post("/api/v1/kyc/verify-dossier", data={
        "applicant_id": "APP-K02",
        "gstin": "19E0GXH4115Y1ZL",
        "udyam_no": "UDYAM-WB-00-5053330",
        "signatory_name": "Joseph Shah",
        "pincode": "347550",
        "dpdp_consent": "true"
    })
    print("K02 response:", res.status_code, res.json())
    assert res.status_code == 200
    assert res.json()["verification_verdict"] == "REJECTED"
    assert "CRITICAL" in str(res.json()["security_flags"])

def test_k03():
    # K03: Joseph Singh / Ganesh Woodcraft (Clean active GSTIN & Udyam)
    res = client.post("/api/v1/kyc/verify-dossier", data={
        "applicant_id": "APP-K03",
        "gstin": "27XUIXG0767D1ZP",
        "udyam_no": "UDYAM-MH-00-9516696",
        "signatory_name": "Joseph Singh",
        "pincode": "411231",
        "dpdp_consent": "true"
    })
    print("K03 response:", res.status_code, res.json())
    assert res.status_code == 200
    assert res.json()["verification_verdict"] == "AUTO_APPROVED"

def test_recommendation():
    res = client.post("/api/v1/catalog/recommend", json={
        "business_type": "Kirana / Retail",
        "employee_count": 4,
        "num_sites": 1,
        "has_gstin": True,
        "city_tier": 1,
        "budget_inr": 2500,
        "requires_calling_sims": True,
        "preferred_language": "en"
    })
    assert res.status_code == 200
    data = res.json()
    assert len(data["bundles"]) == 3
    print("Bundle 1:", data["bundles"][0]["title"], data["bundles"][0]["total_mrc"])

def test_analytics():
    res = client.get("/api/v1/analytics/funnel")
    assert res.status_code == 200
    data = res.json()
    assert data["total_leads"] == 5000
    assert data["activated_leads"] == 368
    print("Funnel data:", data)

    res_q = client.get("/api/v1/analytics/propensity-queue?limit=10")
    assert res_q.status_code == 200
    q = res_q.json()
    assert len(q) > 0
    print("Top lead in queue:", q[0]["business_name"], q[0]["propensity_score"], q[0]["priority"])

if __name__ == "__main__":
    test_health()
    test_k01()
    test_k02()
    test_k03()
    test_recommendation()
    test_analytics()
    print("\nALL BACKEND TESTS PASSED!")

