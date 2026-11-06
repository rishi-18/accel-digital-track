# Antigravity System Prompt: Project Udyam Digital
## B2B MSME Digital Onboarding Platform (Zero-Trust & High-Assurance Edition)

---

## 1. Executive Context & Objectives

You are building **Project Udyam Digital** for Accel Telecom's B2B enterprise division (**Accel Business**).
* **The Mission:** Transform a slow, 17.6-day paper-heavy sales cycle into a self-service, multilingual digital acquisition and activation journey that onboards Indian MSMEs (kirana stores, clinics, coaching centres, professional offices, and small manufacturers) in under 48 hours with minimal human touch.
* **The Business Problem:**
  * Only 7.36% of leads convert to activation (368 out of 5,000 leads).
  * 56% drop-off between *Needs Assessed* and *Quote Accepted* due to pricing opacity, competitor offers, multi-day delays, and technical PDF jargon.
  * 31.7% drop-off post-quote acceptance due to cumbersome paperwork, missing registrations, and delivery delays.
  * High blended Customer Acquisition Cost (CAC) of ₹15,000 per customer against an average micro-bundle value of ₹2,500/month.
  * Customers chase status updates an average of 3.0 times per lead.
* **Deliverable Requirement:** A dual-interface application:
  1. **Customer Onboarding Portal (`/`):** Mobile-first PWA experience (390px-430px centered viewport container) with conversational discovery, real-time bill configuration, instant KYC with defect detection, and a live fulfillment milestone tracker.
  2. **Partner & Sales Back-Office Console (`/partner-desk`):** 1024px+ desktop dashboard analyzing historical drop-offs from `smb_leads.csv`, calculating a propensity recovery score, and surfacing flagged KYC documents for assisted triage.

---

## 2. Threat Landscape & Zero-Trust Security Specifications

Because the application handles statutory business registrations, tax IDs (GSTIN/Udyam), signatory identities, and billing proofs, it must strictly comply with India's **Digital Personal Data Protection (DPDP) Act, 2023** and defend against adversarial vectors:

1. **Direct Injection & Model Manipulation:**
   * LLMs must operate as **untrusted, read-only intent extractors and text articulators**.
   * The AI model must **never** compute prices, apply discounts, or alter database states.
   * All pricing, catalog constraints, and dependencies from `product_catalogue.csv` are calculated by a deterministic backend rule engine.
   * Enforce strict Pydantic/Zod JSON schema decoders. Any output violating the schema must be discarded immediately.

2. **DPDP Act (2023) Compliance & Data Minimization:**
   * **Purpose-Limited Consent:** Unbundled, explicit checkbox required before uploading documents or executing queries. Processing without consent returns HTTP 400.
   * **Zero Disk Persistence (Ephemeral Ingestion):** Uploaded files must be processed exclusively in volatile memory buffers (`io.BytesIO` / RAM tmpfs). Raw files must **never be written to disk, local storage, or public buckets**. The buffer is zeroed and freed immediately after OCR hashing.
   * **PII Redaction Vault:** Automatically redact national identity numbers (masking the first 8 digits of Aadhaar/ID numbers to `XXXX-XXXX-1234`) both client-side on canvas upload and server-side in logs.
   * **Auditability:** Store only `SHA-256(raw_bytes)`, verification timestamps, and validation statuses.

3. **Planted Defect Interception (Specimen Suite K01–K12):**
   * **Structural Format Checks:** Enforce statutory 15-character GSTIN regex (`^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$`). Catch synthetic planted defects like `K02_gst_certificate.png` (which contains `19E0GXH...` with an invalid numeric zero in the PAN block). Note: The synthetic dataset uses `X` in character 4; this is explicitly allowed.
   * **Mandatory Field Completeness:** Detect and flag missing values, such as `K01_udyam_certificate.png` where the Udyam number is empty.
   * **State-Pincode Geofencing:** Validate that the address pincode aligns with the state GST code (e.g., flag Andhra Pradesh `37` with Northern PIN `118383` in K01, or Kolkata with Rajasthan PIN `347550` in K02).
   * **Fuzzy Cross-Matching:** Compute Token Set Ratio / Levenshtein distance between the Signatory ID Name and the Legal Proprietor Name in `mock_gstin_registry.csv`. Score $< 80\%$ triggers an `UNVERIFIED_SIGNATORY` warning.

4. **Tamper-Proof Session & Tracking Security:**
   * Order tracking routes (`/tracker?order=...`) must use cryptographically secure UUIDv4 identifiers coupled with HMAC-SHA256 signatures to prevent ID enumeration.

---

## 3. Tech Stack & Design System

* **Framework:** Next.js (App Router), TypeScript, Tailwind CSS, Lucide React icons.
* **Backend:** FastAPI (Python) or Next.js Route Handlers with integrated Pydantic validation.
* **Algorithms:** Constraint Satisfaction Problem (CSP) for catalog optimization, Token Set Ratio (`thefuzz` / `rapidfuzz`) for cross-document reconciliation, and Heuristic Propensity Scoring for partner recovery.
* **Color Palette:**
  * **Primary Accent:** Telecom Brand Red (`#E40000` / `#DC2626`)
  * **Enterprise Navy / Slate:** `#0F172A` (Text), `#1E293B` (Headings/Borders)
  * **Verified Status Green:** `#16A34A` (Pass badges, active progress)
  * **Warning / Alert Amber:** `#EA580C` (Soft mismatches, assisted flags)
  * **Surfaces:** `#F8FAFC` (Page background), `#FFFFFF` (Cards), `#E2E8F0` (Dividers)
* **Responsive Layout Strategy:**
  * `/` (Customer Portal): Mobile-first container (`max-w-md`, ~390px-430px wide, min-h-[844px], rounded-3xl shadow-2xl on desktop, full-width on mobile devices).
  * `/partner-desk` (Back-Office): Full-width desktop operations layout with metrics, filterable tables, and audit drawers.

---

## 4. Synthetic Data Integration

Load the following dataset files directly into memory:
* `product_catalogue.csv` (25 products): Product catalog with price ranges, setup fees, contract tenures, eligibility rules, and dependencies (`requires_one_of`, `requires_gstin`).
* `mock_gstin_registry.csv` (3,534 records): Backing data for GSTIN lookup API (legal name, trade name, status, state, address).
* `mock_udyam_registry.csv` (2,723 records): Backing data for MSME Udyam lookup API.
* `smb_leads.csv` (5,000 leads): Historical funnel data powering conversion KPIs and drop-off propensity scoring.
* `kyc_documents/` (Specimens K01–K12): Reference documents containing planted defects.

---

## 5. Customer Onboarding Journey (`/`)

### Screen 1: Multimodal Conversational Advisor
* **Bilingual Switcher:** Toggle between English and हिंदी / Hinglish in the header.
* **Input Modes:** Conversational text input, quick-reply buttons (e.g., *"🏪 Kirana / Retail"*, *"🩺 Clinic / Diagnostic"*, *"📚 Coaching / Office"*, *"🏭 Small Factory"*), and a mock voice-mic button (*"Speak in Hindi"*).
* **Needs Extraction Schema:** Extracts `business_type`, `employee_count`, `has_gstin`, `requires_calling_sims`, `budget`.
* **Deterministic CSP Bundle Matcher:**
  * Filters out SKUs violating `min_employees`, `min_sites`, or `available_city_tiers`.
  * If `has_gstin == false`, excludes products where `requires_gstin == 'Y'`.
  * Resolves dependency requirements (`requires_one_of`).
* **Curated Recommendation Cards:** Generates 3 tiered bundles (e.g., *Dukaan Starter*, *Office Pro Connect*, *Enterprise Multi-Store*) with a plain-language summary explaining *why* it was configured for their business.

### Screen 2: Dynamic Bundle Configurator & Checkout
* **Transparent Breakdown:** Displays unified Monthly Recurring Charge (MRC) and one-time setup fee.
* **Interactive Add-On Toggles:** Real-time recalculation when adding Static IP, Extra SIMs, Cloud Storage, or CCTV Links.
* **Contract Duration Switcher:** 12 Months vs. 24 Months (shows upfront setup fee waived to ₹0 on 12+ month commitments).
* **CTA Button:** *"Lock Monthly Plan & Verify Instant KYC"*.

### Screen 3: Smart KYC & DPDP Compliance
* **Consent Screen:** Explicit DPDP Act 2023 consent checkbox.
* **Fast-Track Registry Lookup:** Input GSTIN or Udyam number with a 1-tap *"Fetch Details"* button to auto-fill legal entity name and address.
* **Document Verification / Demo Fixtures:**
  * File upload zone with drag-and-drop support.
  * Provide **Instant Demo Buttons** for testing live before the judges:
    * `Load Sample K01`: Loads Neha Kaur / Vindhya Tours (demonstrating missing Udyam + pincode flag $\rightarrow$ Routes to Assisted Desk).
    * `Load Sample K02`: Loads Joseph Shah / Harmony Dental (demonstrating skewed image + malformed GSTIN `19E0...` $\rightarrow$ Rejected).
    * `Load Sample K03`: Loads Joseph Singh / Ganesh Woodcraft (demonstrating 100% clean verification $\rightarrow$ Auto-Approved).
* **Decision States:**
  * `AUTO_APPROVED`: Clean match $\rightarrow$ immediate transition to order confirmation.
  * `ASSISTED_REVIEW`: Soft mismatch $\rightarrow$ shows reassurance banner: *"Document flagged for quick partner verification. Your installation slot is reserved."*
  * `REJECTED`: Critical syntax violation or cancelled registry record.

### Screen 4: Real-Time Order Tracker (`/tracker`)
* **Milestone Progress Bar:** `[✓] Plan Selected` $\rightarrow$ `[✓] KYC Verified` $\rightarrow$ `[◎] Hardware Dispatch` $\rightarrow$ `[○] Installation & Activation`.
* **Technician Dispatch Card:** Shows technician name, slotted installation window (under 24 hours), and direct 1-tap WhatsApp and Phone contact triggers to eliminate status chasing.

---

## 6. Partner & Sales Back-Office Dashboard (`/partner-desk`)

Build an enterprise operations console that empowers field agents and channel partners:

* **Executive Funnel Metrics:**
  * Cards displaying figures computed from `smb_leads.csv`: Total Leads (5,000), Conversion Rate (7.36%), Median Lead-to-Activation (17.6 days), Average Status Chases (3.0 calls), Current Blended CAC (₹15,000).
* **Drop-Off Propensity Queue:**
  * Filter leads that dropped at `Needs assessed` or `Quote accepted`.
  * Calculate and rank leads by a **Propensity Score (0–100)**:
    * `+30` if `has_gstin == 'Y'` (data confirms 9.6% vs 2.0% activation rate).
    * `+25` if reached `Quote accepted`.
    * `+15` if `num_sites > 1`.
    * `+15` if drop reason was operational (`"Paperwork too long"` or `"Quote took too long to arrive"`).
  * Priority badges: `High Priority (Score ≥ 65)`, `Medium Priority`, `Low Priority`.
* **Lead Inspection & Intervention Drawer:**
  * Inspect applicant profile, dropped stage, and OCR failure reason.
  * Action triggers: *"Dispatch Assisted WhatsApp KYC Link"* and *"Assign Field Rep"*.

---

## 7. Hardened FastAPI Verification Code

Ensure the backend contains this complete, hardened Python endpoint:

```python
import io
import re
import secrets
import hashlib
import hmac
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from thefuzz import fuzz
import pandas as pd

app = FastAPI(
    title="Accel Project Udyam - Zero-Trust Onboarding Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

APP_SECRET = secrets.token_hex(32)

# Load mock datasets into memory
try:
    gstin_df = pd.read_csv('mock_gstin_registry.csv')
    udyam_df = pd.read_csv('mock_udyam_registry.csv')
except Exception:
    gstin_df = pd.DataFrame(columns=['gstin', 'legal_name', 'trade_name', 'status', 'state'])
    udyam_df = pd.DataFrame(columns=['udyam_number', 'enterprise_name', 'status'])

STATE_PIN_PREFIX = {
    "19": ("West Bengal", ["70", "71", "72", "73", "74"]),
    "27": ("Maharashtra", ["40", "41", "42", "43", "44"]),
    "37": ("Andhra Pradesh", ["51", "52", "53"])
}

class KYCVerificationResponse(BaseModel):
    session_id: str
    document_hash: str
    gstin_status: str
    udyam_status: str
    identity_match_score: int
    security_flags: List[str]
    verification_verdict: str
    signed_token: str

def mask_pii(text: str) -> str:
    """Masks 12-digit numbers for display and logs."""
    return re.sub(r"\b(\d{4})[- ]?(\d{4})[- ]?(\d{4})\b", r"XXXX-XXXX-\3", text)

def validate_gstin_syntax(gstin: str) -> tuple[bool, str]:
    gstin = gstin.strip().upper()
    if len(gstin) != 15:
        return False, "GSTIN must be exactly 15 characters long."
    
    # 2 digits + 5 chars (PAN) + 4 digits + 1 char + 1 entity num + 'Z' + 1 checksum
    # Hackathon synthetic dataset uses 'X' in character 4; accept standard alphanumeric
    regex_pattern = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    if not re.match(regex_pattern, gstin):
        return False, f"Malformed GSTIN: '{gstin}' violates entity format rules."
    return True, "Valid syntax."

@app.post("/api/v1/kyc/verify-dossier", response_model=KYCVerificationResponse)
async def verify_kyc_dossier(
    applicant_id: str = Form(...),
    gstin: str = Form(...),
    udyam_no: Optional[str] = Form(None),
    signatory_name: str = Form(...),
    pincode: Optional[str] = Form(None),
    dpdp_consent: bool = Form(...),
    file: Optional[UploadFile] = File(None)
):
    if not dpdp_consent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DPDP Consent must be explicitly granted for business verification."
        )

    security_flags = []
    doc_hash = "no_file_uploaded"

    if file:
        raw_bytes = await file.read()
        if len(raw_bytes) > 5 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Payload exceeds 5MB limit.")
        
        header = raw_bytes[:4]
        is_pdf = header == b"%PDF"
        is_png = header.startswith(b"\x89PNG")
        is_jpeg = header.startswith(b"\xff\xd8\xff")
        if not (is_pdf or is_png or is_jpeg):
            raise HTTPException(status_code=415, detail="Unsupported binary format.")

        doc_hash = hashlib.sha256(raw_bytes).hexdigest()

    # 1. GSTIN Validation
    is_syntax_valid, syntax_msg = validate_gstin_syntax(gstin)
    gst_status = "UNKNOWN"
    gst_legal_name = ""

    if not is_syntax_valid:
        security_flags.append(f"CRITICAL: {syntax_msg}")
        gst_status = "SYNTAX_VIOLATION"
    else:
        matched_gst = gstin_df[gstin_df['gstin'] == gstin.strip().upper()]
        if matched_gst.empty:
            security_flags.append("WARNING: GSTIN not found in active commercial tax register.")
            gst_status = "NOT_FOUND"
        else:
            reg_status = matched_gst.iloc[0].get('status', 'Active')
            gst_legal_name = str(matched_gst.iloc[0].get('legal_name', ''))
            if reg_status != 'Active':
                security_flags.append(f"CRITICAL: Registry records GSTIN as '{reg_status}'.")
                gst_status = f"REGISTRY_{reg_status.upper()}"
            else:
                gst_status = "VERIFIED_ACTIVE"

    # 2. Udyam Validation
    udyam_status = "NOT_PROVIDED"
    if not udyam_no or not udyam_no.strip():
        security_flags.append("FLAG: Udyam Registration number missing or blank on document.")
        udyam_status = "MISSING_NUMBER"
    else:
        u_clean = udyam_no.strip().upper()
        if not re.match(r"^UDYAM-[A-Z]{2}-[0-9]{2}-[0-9]{7}$", u_clean):
            security_flags.append(f"FLAG: Udyam number '{u_clean}' has invalid schema.")
            udyam_status = "INVALID_SYNTAX"
        else:
            matched_u = udyam_df[udyam_df['udyam_number'] == u_clean]
            if matched_u.empty:
                security_flags.append("FLAG: Udyam ID not present in MSME database.")
                udyam_status = "UNREGISTERED"
            else:
                udyam_status = "VERIFIED"

    # 3. Fuzzy Name Match & Geofencing
    name_score = 0
    if gst_legal_name:
        name_score = fuzz.token_set_ratio(signatory_name.strip(), gst_legal_name)
        if name_score < 80:
            security_flags.append(
                f"AUDIT: Signatory '{mask_pii(signatory_name)}' does not match Legal Name "
                f"'{mask_pii(gst_legal_name)}' (Fuzzy Score: {name_score}%)"
            )

    if pincode and len(gstin) >= 2:
        st_code = gstin[:2]
        if st_code in STATE_PIN_PREFIX:
            expected_state, valid_prefixes = STATE_PIN_PREFIX[st_code]
            if not any(str(pincode).startswith(pfx) for pfx in valid_prefixes):
                security_flags.append(
                    f"ANOMALY: Postal code '{pincode}' does not align with state '{expected_state}'."
                )

    # 4. Final Verdict
    if any("CRITICAL" in flag for flag in security_flags):
        verdict = "REJECTED"
    elif security_flags:
        verdict = "ASSISTED_REVIEW"
    else:
        verdict = "AUTO_APPROVED"

    token_payload = f"{applicant_id}:{verdict}:{doc_hash}"
    signed_token = hmac.new(
        APP_SECRET.encode(),
        token_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return KYCVerificationResponse(
        session_id=secrets.token_urlsafe(16),
        document_hash=doc_hash,
        gstin_status=gst_status,
        udyam_status=udyam_status,
        identity_match_score=name_score,
        security_flags=security_flags,
        verification_verdict=verdict,
        signed_token=signed_token
    )
```

---

## 8. Final Evaluation Checklist
Before shipping the prototype, verify:
- [ ] No file uploaded is ever stored persistently on disk.
- [ ] Prices and bundles match `product_catalogue.csv` rules exactly.
- [ ] Mobile-first viewport container (`max-w-md`) is rendered on the `/` customer route, while `/partner-desk` renders a full-width desktop view.
- [ ] Presets for applicants `K01`, `K02`, and `K03` are easily selectable in the UI to demonstrate defect handling live during judging.