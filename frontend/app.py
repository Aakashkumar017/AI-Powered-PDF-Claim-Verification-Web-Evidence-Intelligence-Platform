import streamlit as st
import requests
import json
import os  # Added for environment variable management

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GEO Fact Checker",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #050816;
    color: white;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1200px; padding-top: 2rem; padding-bottom: 4rem; }

/* HERO */
.hero { padding: 3rem 0 2rem 0; }
.hero-title { font-size: 3.6rem; font-weight: 700; line-height: 1.1; margin-bottom: 1rem; }
.hero-title span { color: #00d084; }
.hero-sub { color: #8b9bb4; font-size: 1.05rem; max-width: 720px; line-height: 1.8; }
.tag-row { display: flex; gap: 12px; margin-top: 2rem; margin-bottom: 2rem; flex-wrap: wrap; }
.tag { background: #0d1324; border: 1px solid #1c2742; padding: 10px 16px; border-radius: 12px; color: #dce6ff; font-size: 0.85rem; }

/* UPLOAD CONTAINER */
div[data-testid="stFileUploader"] {
    background: #0b1120; 
    border: 1px solid #1b2640; 
    border-radius: 20px; 
    padding: 24px; 
    margin-top: 2rem; 
    margin-bottom: 2rem;
}

/* KPI */
.metric-card { background: linear-gradient(180deg,#0b1120,#0a0f1c); border: 1px solid #18233d; padding: 28px; border-radius: 18px; text-align: center; }
.metric-number { font-size: 2.8rem; font-weight: 700; }
.metric-label { color: #7d8ba8; font-size: 0.8rem; margin-top: 8px; }

/* CLAIM CARDS */
.claim-card {
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    transition: border-color 0.2s;
}
.claim-card.verified  { background: #071a10; border: 1px solid #00d08440; }
.claim-card.refuted   { background: #1a0707; border: 1px solid #ff5c5c40; }
.claim-card.uncertain { background: #1a1407; border: 1px solid #ffb80040; }

.claim-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; }
.claim-status { padding: 8px 14px; border-radius: 999px; font-size: 0.75rem; font-weight: 600; }
.claim-title { font-size: 1.1rem; font-weight: 500; line-height: 1.7; }

.status-verified  { background: rgba(0,208,132,0.15);  color: #00d084; }
.status-refuted   { background: rgba(255,77,77,0.15);   color: #ff5c5c; }
.status-uncertain { background: rgba(255,184,0,0.15);   color: #ffb800; }

/* EVIDENCE */
.section-label { color: #7d8ba8; font-size: 0.78rem; margin-bottom: 10px; margin-top: 18px; text-transform: uppercase; letter-spacing: 1px; }
.evidence-box  { background: #09101d; border: 1px solid #18233d; border-radius: 12px; padding: 18px; line-height: 1.8; color: #c8d3ea; }
.correct-box   { background: #071a10; border-left: 4px solid #00d084; border-radius: 0 12px 12px 0; padding: 18px; line-height: 1.8; color: #c8d3ea; }

/* SOURCES */
.source-link { display: inline-block; margin-bottom: 8px; margin-right: 8px; color: #42a5ff; text-decoration: none; font-size: 0.88rem; background: #0b1630; border: 1px solid #1a2d50; padding: 5px 12px; border-radius: 8px; }
.source-link:hover { color: white; background: #152040; }

/* CONFIDENCE */
.confidence-box { text-align: center; padding: 12px; }
.confidence-number { font-size: 2.8rem; font-weight: 700; line-height: 1; }
.confidence-label  { color: #7d8ba8; font-size: 0.75rem; margin-bottom: 8px; }

.conf-high { color: #00d084; }
.conf-mid  { color: #ffb800; }
.conf-low  { color: #ff5c5c; }

.small-muted { color: #7d8ba8; font-size: 0.8rem; }

/* SUMMARY BAR */
.summary-bar {
    background: #0b1120;
    border: 1px solid #1a2744;
    border-radius: 14px;
    padding: 16px 24px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
}
.acc-score { font-size: 2rem; font-weight: 700; color: #00d084; }
.acc-label { color: #7d8ba8; font-size: 0.82rem; }
</style>
""", unsafe_allow_html=True)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div style="font-size:0.9rem;color:#00d084;margin-bottom:12px;letter-spacing:1px;">
    AI-POWERED CLAIM VERIFICATION
  </div>
  <div class="hero-title">Every Claim.<br><span>Verified.</span></div>
  <div class="hero-sub">
    Upload any PDF document. GEO extracts factual claims, searches live web
    evidence, and returns verdicts with confidence scores and sources.
  </div>
  <div class="tag-row">
    <div class="tag">⚡ Groq · Llama 3.3 70B</div>
    <div class="tag">🌐 Tavily Live Search</div>
    <div class="tag">📄 PyMuPDF Extraction</div>
    <div class="tag">🧠 AI Reasoning Engine</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── UPLOAD ─────────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    label_visibility="collapsed",
    help="Max 200 MB. Text-based PDFs only (scanned images not supported).",
)

if not uploaded_file:
    st.info("📄 Upload a PDF above to begin AI-powered fact verification.")
    st.stop()

# ── API CALL ───────────────────────────────────────────────────────────────────
# Fixed: Read production URL dynamically from environment variables
BACKEND_BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
BACKEND_URL = f"{BACKEND_BASE_URL.rstrip('/')}/fact-check"

progress_placeholder = st.empty()
with progress_placeholder:
    with st.spinner("🔍 Extracting and verifying claims — this may take 30–60 seconds…"):
        try:
            # Fixed: Repositioned variable definition safely to the left 
            response = requests.post(
                BACKEND_URL,
                files={"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")},
                timeout=180
            )
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot reach the backend at {BACKEND_URL}. Make sure your API is up.")
            st.stop()
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Try a shorter document.")
            st.stop()
        except Exception as e:
            st.error("Unexpected error contacting backend.")
            st.exception(e)
            st.stop()

progress_placeholder.empty()

if response.status_code != 200:
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text
    st.error(f"Backend error ({response.status_code}): {detail}")
    st.stop()

data    = response.json()
results = data.get("results", [])

if not results:
    st.warning(data.get("message", "No verifiable factual claims were found in this document."))
    st.stop()

# ── HELPERS ────────────────────────────────────────────────────────────────────
_REFUTED = {"FALSE", "INACCURATE", "REFUTED", "INCORRECT", "WRONG"}

def card_class(status: str) -> str:
    s = status.upper()
    if s == "VERIFIED":  return "verified"
    if s in _REFUTED:    return "refuted"
    return "uncertain"

def badge_class(status: str) -> str:
    return f"status-{card_class(status)}"

def normalise_conf(raw) -> int:
    try:
        v = float(str(raw).replace("%", "").strip())
        if v <= 1.0: v *= 100
        return max(0, min(100, int(v)))
    except Exception:
        return 0

def conf_color_class(conf: int) -> str:
    if conf >= 75: return "conf-high"
    if conf >= 45: return "conf-mid"
    return "conf-low"

# ── KPI COUNTERS ───────────────────────────────────────────────────────────────
verified = sum(1 for r in results if r.get("status","").upper() == "VERIFIED")
refuted  = sum(1 for r in results if r.get("status","").upper() in _REFUTED)
uncertain = len(results) - verified - refuted

verdict_total = verified + refuted
accuracy = int(verified / verdict_total * 100) if verdict_total else 0

# Summary bar
st.markdown(f"""
<div class="summary-bar">
  <div>
    <div class="acc-score">{accuracy}%</div>
    <div class="acc-label">Accuracy Rate</div>
  </div>
  <div style="width:1px;height:40px;background:#1a2744;"></div>
  <div style="flex:1;color:#8b9bb4;font-size:0.9rem;">
    Checked <strong style="color:white">{len(results)}</strong> claims —
    <strong style="color:#00d084">{verified} verified</strong>,
    <strong style="color:#ff5c5c">{refuted} refuted</strong>,
    <strong style="color:#ffb800">{uncertain} uncertain</strong>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
for col, num, label, color in [
    (col1, len(results), "Claims Checked", "white"),
    (col2, verified,     "Verified",       "#00d084"),
    (col3, refuted,      "Refuted",        "#ff5c5c"),
    (col4, uncertain,    "Uncertain",      "#ffb800"),
]:
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-number" style="color:{color};">{num}</div>
          <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── FILTER TABS ────────────────────────────────────────────────────────────────
st.subheader("Claim Analysis")

filter_tab = st.radio(
    "Filter",
    ["All", "Verified", "Refuted", "Uncertain"],
    horizontal=True,
    label_visibility="collapsed",
)

def matches_filter(status: str) -> bool:
    s = status.upper()
    if filter_tab == "All":       return True
    if filter_tab == "Verified":  return s == "VERIFIED"
    if filter_tab == "Refuted":   return s in _REFUTED
    if filter_tab == "Uncertain": return s not in ({"VERIFIED"} | _REFUTED)
    return True

st.markdown("<br>", unsafe_allow_html=True)

# ── CLAIM CARDS ────────────────────────────────────────────────────────────────
shown = 0
for index, item in enumerate(results):
    claim        = item.get("claim", "")
    status       = item.get("status", "UNCERTAIN").upper()
    explanation  = item.get("explanation", "No explanation provided.")
    correct_fact = item.get("correct_fact", "")
    conf         = normalise_conf(item.get("confidence", 0))
    sources      = item.get("sources", [])

    if not matches_filter(status):
        continue
    shown += 1

    cc  = card_class(status)
    bc  = badge_class(status)
    ccl = conf_color_class(conf)

    st.markdown(f"""
    <div class="claim-card {cc}">
      <div class="claim-top">
        <div class="claim-status {bc}">{status}</div>
        <div class="small-muted">#{index + 1}</div>
      </div>
      <div class="claim-title">{claim}</div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("View evidence & sources"):
        left, right = st.columns([4, 1])

        with left:
            if correct_fact and correct_fact.lower() != claim.lower():
                st.markdown('<div class="section-label">✅ Correct Information</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="correct-box">{correct_fact}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label">🧠 AI Reasoning</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="evidence-box">{explanation}</div>', unsafe_allow_html=True)

            if sources:
                st.markdown('<div class="section-label">🔗 Sources</div>', unsafe_allow_html=True)
                links = "".join(
                    f'<a class="source-link" href="{src}" target="_blank">↗ {src[:60]}{"…" if len(src)>60 else ""}</a>'
                    for src in sources
                )
                st.markdown(links, unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div class="confidence-box">
              <div class="confidence-label">Confidence</div>
              <div class="confidence-number {ccl}">{conf}%</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(conf / 100)

if shown == 0:
    st.info("No claims match this filter.")

# ── DOWNLOAD ───────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)

col_a, col_b = st.columns([1, 3])
with col_a:
    st.download_button(
        label="📥 Download JSON Report",
        data=json.dumps({"summary": {"total": len(results), "verified": verified,
                                      "refuted": refuted, "uncertain": uncertain,
                                      "accuracy_rate": f"{accuracy}%"},
                          "results": results}, indent=2),
        file_name="fact_check_report.json",
        mime="application/json",
        use_container_width=True,
    )