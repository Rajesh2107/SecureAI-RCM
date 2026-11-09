
import os
import json
import requests
import streamlit as st
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")
AUDIT_FILE = "/app/logs/security_audit.jsonl"

st.set_page_config(
    page_title="SecureAI-RCM | Command Center",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#07111f,#0b1728 55%,#101e32);color:#e8f0fa}
[data-testid="stHeader"] {background:transparent}
[data-testid="stSidebar"] {display:none}
.block-container {max-width:1600px;padding-top:1.2rem;padding-bottom:2rem}
h1,h2,h3 {color:#f3f7ff!important}
p,label {color:#d5e2f2}
div[data-testid="stMetric"] {background:linear-gradient(145deg,#13243a,#102033);border:1px solid #263c56;padding:18px;border-radius:16px}
div[data-testid="stMetricLabel"] {color:#9fb7d2}
div[data-testid="stMetricValue"] {color:#55e0c0;font-weight:750}
.stButton>button {background:linear-gradient(90deg,#0ea5a4,#18c7a5);color:#06202a;border:0;border-radius:10px;font-weight:700}
div[data-testid="stDataFrame"] {border:1px solid #263c56;border-radius:12px}
.hero {background:linear-gradient(110deg,#122840,#123b4b);border:1px solid #28536a;border-radius:20px;padding:24px 28px;margin-bottom:18px}
.eyebrow {color:#55e0c0;text-transform:uppercase;letter-spacing:2px;font-size:12px;font-weight:800}
.hero-title {font-size:32px;font-weight:800;color:#f4f8ff;margin:5px 0}
.hero-sub {color:#b8cce0;font-size:14px}
.pill {display:inline-block;background:#123d38;color:#70f0cf;border:1px solid #22685a;border-radius:30px;padding:5px 11px;font-size:12px;font-weight:700}
</style>
""", unsafe_allow_html=True)


def api_get(endpoint):
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=180)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        st.error(f"API issue: {exc}")
        return None


def status_of(claim):
    return str(claim.get("status", "")).strip().lower()


# HEADER
st.markdown("""
<div class="hero">
  <div class="eyebrow">Healthcare AI - Security &amp; Governance</div>
  <div class="hero-title">SecureAI-RCM <span class="pill">COMMAND CENTER</span></div>
  <div class="hero-sub">Revenue Cycle Intelligence | Grounded AI Denial Insights | Security Monitoring</div>
</div>
""", unsafe_allow_html=True)


# CLAIMS
claims_response = api_get("/claims")
claims = (
    claims_response.get("claims", [])
    if isinstance(claims_response, dict)
    else (claims_response or [])
)
claims = claims if isinstance(claims, list) else []

total = len(claims)
denied_claims = [c for c in claims if status_of(c) == "denied"]
approved_claims = [c for c in claims if status_of(c) == "approved"]
pending_claims = [c for c in claims if status_of(c) == "pending"]


# PORTFOLIO
st.markdown("## Portfolio Overview")

k1, k2, k3, k4 = st.columns(4)
k1.metric("TOTAL CLAIMS", total)
k2.metric("DENIED", len(denied_claims),
          f"{len(denied_claims)/total*100:.0f}% of portfolio" if total else None)
k3.metric("APPROVED", len(approved_claims),
          f"{len(approved_claims)/total*100:.0f}% of portfolio" if total else None)
k4.metric("PENDING", len(pending_claims))


# CLAIMS REGISTER
st.markdown("## Claims Register")

if claims:
    claims_df = pd.DataFrame(claims)

    if "status" in claims_df.columns:
        claims_df["status"] = claims_df["status"].astype(str).str.upper()

    st.dataframe(
        claims_df,
        use_container_width=True,
        hide_index=True,
        height=350
    )

    status_counts = pd.DataFrame({
        "Status": ["Denied", "Approved", "Pending"],
        "Claims": [
            len(denied_claims),
            len(approved_claims),
            len(pending_claims)
        ]
    }).set_index("Status")

    st.markdown("### Claim Status Distribution")
    st.bar_chart(status_counts, use_container_width=True)

else:
    st.warning("Claims could not be loaded.")


# AI DENIAL INTELLIGENCE
st.markdown("## AI Denial Intelligence")

if denied_claims:
    claim_ids = [c.get("claim_id", "Unknown") for c in denied_claims]
    chosen = st.selectbox("Select denied claim", claim_ids)

    selected = next(
        (c for c in denied_claims if c.get("claim_id") == chosen),
        denied_claims[0]
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Claim ID", chosen)
    col2.metric("Payer", selected.get("payer", "—"))
    col3.metric("Service", selected.get("service", "—"))

    with st.spinner("Loading AI explanation..."):
        explanation_response = api_get(f"/ai/explain/{chosen}")

    if explanation_response:
        explanation = explanation_response.get(
            "ai_explanation",
            explanation_response.get("explanation", explanation_response)
        )

        st.markdown("### AI Explanation")

        if isinstance(explanation, str):
            st.write(explanation)
        else:
            st.json(explanation)

        st.success("Explanation loaded - Grounded in available claim context")
        st.warning("Advisory only - Human review required")

    else:
        st.info("AI explanation unavailable. Check backend and Ollama.")

else:
    st.info("No denied claims available.")


# SECURITY AUDIT
st.markdown("## Security & Audit")

audit_events = []
audit_available = os.path.exists(AUDIT_FILE)

if audit_available:
    try:
        with open(AUDIT_FILE, encoding="utf-8") as audit_file:
            audit_events = [
                json.loads(line)
                for line in audit_file
                if line.strip()
            ]
    except Exception as exc:
        st.error(f"Audit log read error: {exc}")

audit_col1, audit_col2, audit_col3 = st.columns(3)

audit_col1.metric("TOTAL AUDIT EVENTS", len(audit_events))
audit_col2.metric("EVENTS DISPLAYED", len(audit_events))
audit_col3.metric(
    "AUDIT LOG",
    "AVAILABLE" if audit_available else "NOT FOUND"
)

if audit_events:
    st.dataframe(
        pd.DataFrame(audit_events[::-1]),
        use_container_width=True,
        hide_index=True,
        height=400
    )
else:
    st.info("No audit events yet. Use the API or AI explanation to create events.")


# AI SECURITY LAB
st.markdown("## AI Security Lab")
st.markdown("Validate prompt defenses, PHI handling, and response safety.")

if st.button("▶ Run Security Lab", use_container_width=True):

    with st.spinner("Executing security tests on the backend..."):

        try:
            response = requests.post(
                f"{API_URL}/security/run",
                timeout=130
            )

            response.raise_for_status()
            lab_result = response.json()

            passed = bool(lab_result.get("success", False))

            if passed:
                st.success(
                    lab_result.get(
                        "message",
                        "Security tests completed"
                    )
                )
            else:
                st.error(
                    lab_result.get(
                        "message",
                        "Security tests failed"
                    )
                )

            result_col1, result_col2 = st.columns(2)

            result_col1.metric(
                "TEST RUN STATUS",
                "PASS" if passed else "FAIL"
            )

            result_col2.metric(
                "EXIT CODE",
                lab_result.get("exit_code", "N/A")
            )

            st.markdown("### Execution Output")

            st.code(
                lab_result.get("output", "No output returned"),
                language="text"
            )

        except requests.exceptions.Timeout:
            st.error("Security test execution timed out.")

        except requests.exceptions.HTTPError as exc:
            st.error(
                f"Security endpoint error: "
                f"{exc.response.status_code} - "
                f"{exc.response.text}"
            )

        except Exception as exc:
            st.error(f"Could not execute Security Lab: {exc}")

st.caption(
    "Security Lab results are returned by the actual backend test runner."
)


# FOOTER
st.divider()

st.markdown("""
<div style="display:flex;justify-content:space-between;flex-wrap:wrap;color:#8fa9c3;font-size:12px">
<span>SecureAI-RCM - Portfolio Demonstration</span>
<span>Synthetic data only | Human review mandatory</span>
</div>
""", unsafe_allow_html=True)
