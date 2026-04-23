import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

# To this:
import os
BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="M47 Pathology Dashboard", page_icon="🔬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.stApp { background-color: #F0F4F8; }
section[data-testid="stSidebar"] { background-color: #1A2744 !important; border-right: none !important; }
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span, section[data-testid="stSidebar"] div { color: #CBD5E1 !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
section[data-testid="stSidebar"] .stRadio label { color: #CBD5E1 !important; font-size: 0.92rem; }
section[data-testid="stSidebar"] .stButton>button { background-color: rgba(255,255,255,0.08) !important; color: #F87171 !important; border: 1px solid rgba(248,113,113,0.35) !important; font-weight: 600; }
[data-testid="metric-container"] { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px 24px; }
[data-testid="metric-container"] label { color: #64748B !important; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0F172A !important; font-size: 2rem; font-weight: 700; }
h1 { color: #0F172A !important; font-size: 1.7rem !important; font-weight: 700 !important; padding-bottom: 12px; border-bottom: 3px solid #3B82F6; margin-bottom: 24px; }
h2, h3 { color: #1E293B !important; font-weight: 600 !important; }
p, li { color: #1E293B; }
.stButton>button { background-color: #2563EB !important; color: #FFFFFF !important; border: none !important; border-radius: 8px; font-weight: 600; font-size: 0.9rem; padding: 0.55rem 1.4rem; width: 100%; }
.stButton>button:hover { background-color: #1D4ED8 !important; }
.stTextInput>div>div>input { background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important; border-radius: 8px !important; color: #0F172A !important; }
.stTextInput label { color: #374151 !important; font-weight: 500; font-size: 0.88rem; }
.stSelectbox>div>div { background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important; border-radius: 8px !important; color: #0F172A !important; }
.stSelectbox label { color: #374151 !important; font-weight: 500; font-size: 0.88rem; }
.stDateInput>div>div>input { background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important; border-radius: 8px !important; color: #0F172A !important; }
.stTextArea>div>div>textarea { background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important; border-radius: 8px !important; color: #0F172A !important; }
.stTextArea label, .stDateInput label { color: #374151 !important; font-weight: 500; font-size: 0.88rem; }
hr { border-color: #E2E8F0 !important; margin: 20px 0; }
.card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 14px; padding: 20px 22px; margin-bottom: 14px; }
.card-red   { border-left: 4px solid #EF4444; }
.card-blue  { border-left: 4px solid #3B82F6; }
.card-green { border-left: 4px solid #10B981; }
.card-amber { border-left: 4px solid #F59E0B; }
.card-lbl { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #64748B; margin-bottom: 4px; }
.card-val { font-size: 1.05rem; font-weight: 600; color: #0F172A; margin: 0; }
.card-sub { font-size: 0.82rem; color: #64748B; margin-top: 4px; }
.badge-crit { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.badge-ok   { background-color: #DCFCE7; color: #14532D; border: 1px solid #86EFAC;  padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.badge-pend { background-color: #FEF9C3; color: #713F12; border: 1px solid #FDE047;  padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 700; display: inline-block; }
.sc-red  { color: #DC2626; font-weight: 700; font-size: 1.6rem; }
.sc-green{ color: #059669; font-weight: 700; font-size: 1.6rem; }
.sh { font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 20px 0 12px 0; }
.login-box { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 36px 32px; }
</style>
""", unsafe_allow_html=True)

for k in ["token","username"]:
    if k not in st.session_state: st.session_state[k] = None

def hdr(): return {"Authorization": f"Bearer {st.session_state.token}"}

def get(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", headers=hdr(), timeout=8)
        return r.json() if r.status_code == 200 else None
    except Exception as e:
        st.error(f"Connection error: {e}"); return None

def post(path, payload):
    try: return requests.post(f"{BASE_URL}{path}", json=payload, headers=hdr(), timeout=8)
    except Exception as e: st.error(f"Connection error: {e}"); return None

def login_page():
    _, col, _ = st.columns([1,1.1,1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""<div style='text-align:center;padding:30px 0 28px;'>
            <div style='font-size:3rem;margin-bottom:12px;'>🔬</div>
            <h1 style='border:none!important;padding:0!important;margin:0!important;font-size:1.9rem!important;color:#0F172A!important;'>M47 Oncology</h1>
            <p style='color:#64748B;font-size:0.95rem;margin-top:6px;'>Pathology Report Management System</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="e.g. drsmith")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In →", use_container_width=True):
            try:
                r = requests.post(f"{BASE_URL}/auth/login", data={"username":username,"password":password}, timeout=8)
                if r.status_code == 200:
                    st.session_state.token = r.json()["access_token"]
                    st.session_state.username = username
                    st.success("✅ Login successful!"); st.rerun()
                else: st.error("❌ Invalid credentials. Try: drsmith / doctor123")
            except: st.error("❌ Backend not reachable. Run: uvicorn main:app --reload")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;margin-top:20px;color:#94A3B8;font-size:0.82rem;'>Demo: <b style='color:#2563EB'>drsmith</b> / <b style='color:#2563EB'>doctor123</b> &nbsp;·&nbsp; <b style='color:#2563EB'>admin</b> / <b style='color:#2563EB'>admin123</b></div>", unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        st.markdown(f"""<div style='padding:18px 0 12px;'>
            <div style='font-size:1.2rem;font-weight:700;color:#FFFFFF;'>M47 Pathology</div>
            <div style='font-size:0.82rem;color:#94A3B8;margin-top:3px;'>Dr. {st.session_state.username}</div>
        </div>""", unsafe_allow_html=True)
        st.divider()
        menu = st.radio("Nav", ["📊  Overview","🏥  Patients","📋  Lab Orders","🔬  Pathology Entry","🧬  MDT Session","📈  Prognosis","📁  All Reports"], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True); st.divider()
        if st.button("Logout"):
            st.session_state.token = st.session_state.username = None; st.rerun()
    return menu

def page_overview():
    st.markdown("# 📊 Clinical Overview")
    stats = get("/analysis/stats")
    if stats:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("👤 Patients", stats.get("total_patients",0))
        c2.metric("📋 Reports",  stats.get("total_reports",0))
        c3.metric("🚨 Critical", stats.get("critical_reports",0))
        c4.metric("⏳ Pending MDT", stats.get("pending_mdt",0))
    st.markdown("<br>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sh'>🚨 Critical Reports</div>", unsafe_allow_html=True)
        crit = get("/pathology/critical")
        if crit:
            for r in crit[:5]:
                m = r.get("metrics",{}) or {}
                st.markdown(f"""<div class='card card-red'>
                    <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                        <div><div class='card-lbl'>Report {r.get("Report_ID")} · Patient {r.get("Patient_ID")}</div>
                        <div class='card-val'>T:{m.get("tumor","?")} N:{m.get("node","?")} M:{m.get("metastasis","?")}</div>
                        <div class='card-sub'>Grade: {m.get("grade","?")} · Priority: {r.get("priority","?")}</div></div>
                        <div><span class='badge-crit'>CRITICAL</span>
                        <div style='color:#DC2626;font-weight:700;font-size:1.3rem;text-align:right;margin-top:4px;'>{r.get("automated_score",0)}</div></div>
                    </div></div>""", unsafe_allow_html=True)
        else: st.info("No critical reports.")
    with col2:
        st.markdown("<div class='sh'>📋 Recent MDT Sessions</div>", unsafe_allow_html=True)
        sess = get("/mdt/sessions")
        if sess:
            for s in sess[:4]:
                st.markdown(f"""<div class='card card-blue'>
                    <div class='card-lbl'>{s.get("MDT_ID")} · Patient {s.get("patient_id")}</div>
                    <div class='card-val'>{s.get("decision","—")}</div>
                    <div class='card-sub'>{str(s.get("treatment_plan",""))[:90]}...</div>
                </div>""", unsafe_allow_html=True)
        else: st.info("No MDT sessions.")

def page_patients():
    st.markdown("# 🏥 Patient Registration")
    col1,col2 = st.columns([1,1.2])
    with col1:
        st.markdown("<div class='sh'>Register New Patient</div>", unsafe_allow_html=True)
        p_id = st.text_input("Patient ID", placeholder="e.g. P1011")
        name = st.text_input("Full Name",  placeholder="e.g. Ramesh Gupta")
        dob  = st.date_input("Date of Birth", min_value=date(1920,1,1), value=date(1970,1,1))
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Register Patient"):
            if not p_id or not name: st.warning("Fill in Patient ID and Name.")
            else:
                r = post("/patients", {"Patient_ID":p_id,"name":name,"Date_of_Birth":dob.isoformat(),"gender":gender})
                if r and r.status_code==200: st.success(f"🎉 Patient {name} registered!")
                else: st.error(r.json().get("detail","Error") if r else "No response")
    with col2:
        st.markdown("<div class='sh'>Patient Registry</div>", unsafe_allow_html=True)
        pts = get("/patients")
        if pts:
            df = pd.DataFrame(pts)
            cols = [c for c in ["Patient_ID","name","Date_of_Birth","gender"] if c in df.columns]
            st.dataframe(df[cols].rename(columns={"Patient_ID":"ID","name":"Name","Date_of_Birth":"DOB","gender":"Gender"}), use_container_width=True, hide_index=True)

def page_orders():
    st.markdown("# 📋 Lab Orders")
    col1,col2 = st.columns([1,1.2])
    with col1:
        st.markdown("<div class='sh'>Create Lab Order</div>", unsafe_allow_html=True)
        o_id = st.text_input("Order ID",   placeholder="e.g. LO-011")
        p_id = st.text_input("Patient ID", placeholder="e.g. P1001")
        d_id = st.text_input("Doctor ID",  placeholder="e.g. D001")
        status = st.selectbox("Status", ["Pending","In Progress","Completed"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Create Order"):
            if not o_id or not p_id or not d_id: st.warning("Fill in all fields.")
            else:
                r = post("/orders", {"Order_ID":o_id,"patient_id":p_id,"doctor_id":d_id,"status":status})
                if r and r.status_code==200: st.success(f"✅ Order {o_id} created!")
                else: st.error(r.json().get("detail","Error") if r else "No response")
    with col2:
        st.markdown("<div class='sh'>Existing Orders</div>", unsafe_allow_html=True)
        ords = get("/orders")
        if ords:
            df = pd.DataFrame(ords)
            cols = [c for c in ["Order_ID","patient_id","doctor_id","status"] if c in df.columns]
            st.dataframe(df[cols].rename(columns={"Order_ID":"Order ID","patient_id":"Patient","doctor_id":"Doctor","status":"Status"}), use_container_width=True, hide_index=True)

def page_pathology():
    st.markdown("# 🔬 Pathology Lab Entry")
    st.markdown("<p style='color:#64748B;margin-top:-16px;margin-bottom:24px;'>Process 2.0 & 3.0 — Create report and auto-compute TNM staging score</p>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sh'>Report Details</div>", unsafe_allow_html=True)
        r_id = st.text_input("Report ID",  placeholder="e.g. RPT-009")
        o_id = st.text_input("Order ID",   placeholder="e.g. LO-007 (must exist)")
        p_id = st.text_input("Patient ID", placeholder="e.g. P1007")
        t_id = st.text_input("Test ID",    placeholder="e.g. T047")
        sts  = st.selectbox("Report Status", ["Final","Preliminary","Amended"])
        prio = st.selectbox("Priority",      ["Urgent","High","Routine"])
        rmk  = st.text_area("Remarks",       placeholder="Clinical observations...", height=80)
    with col2:
        st.markdown("<div class='sh'>TNM Cancer Metrics</div>", unsafe_allow_html=True)
        m_id  = st.text_input("Metric ID",      placeholder="e.g. M-009")
        tumor = st.selectbox("Tumor Stage (T)", ["T1","T2","T3","T4"])
        node  = st.selectbox("Node Stage (N)",  ["N0","N1","N2"])
        meta  = st.selectbox("Metastasis (M)",  ["M0","M1"])
        grade = st.selectbox("Grade",           ["G1","G2","G3","High"])
        res   = st.selectbox("Result Type",     ["Biopsy","FNA","IHC","Flow Cytometry"])
        sc = 0
        if meta=="M1": sc+=10
        if tumor in ["T3","T4"]: sc+=5
        if grade in ["G3","High"]: sc+=7
        if node in ["N1","N2"]: sc+=3
        crit = sc>7
        bar_col = "#EF4444" if crit else "#10B981"
        bar_w   = min(int((sc/25)*100),100)
        badge   = "<span class='badge-crit'>CRITICAL — MDT Referral</span>" if crit else "<span class='badge-ok'>Routine Follow-up</span>"
        ac      = "red" if crit else "green"
        sc_cls  = "sc-red" if crit else "sc-green"
        st.markdown(f"""<div class='card card-{ac}' style='margin-top:16px;'>
            <div class='card-lbl'>Live Score Preview</div>
            <div class='{sc_cls}' style='margin:6px 0 2px;'>{sc} <span style='font-size:0.95rem;font-weight:400;color:#64748B;'>/ 25</span></div>
            <div style='background:#F1F5F9;border-radius:6px;height:8px;margin:10px 0;'>
                <div style='background:{bar_col};width:{bar_w}%;height:8px;border-radius:6px;'></div>
            </div>
            {badge}</div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔬 Analyze & Save Report"):
        if not all([r_id,o_id,p_id,t_id,m_id]): st.warning("Fill in all required fields.")
        else:
            payload = {"Report_ID":r_id,"order_id":o_id,"Patient_ID":p_id,"test_id":t_id,"status":sts,"priority":prio,"remarks":rmk,
                "metrics":{"Metric_ID":m_id,"tumor":tumor,"node":node,"metastasis":meta,"result":res,"grade":grade}}
            r = post("/pathology/reports", payload)
            if r and r.status_code==200:
                d = r.json()
                if d.get("is_critical"): st.error(f"⚠️ CRITICAL — Score: {d['automated_score']} · {d['implication']}")
                else: st.success(f"✅ Report saved — Score: {d['automated_score']} · {d['implication']}")
            else: st.error(r.json().get("detail","Error") if r else "No response")

def page_mdt():
    st.markdown("# 🧬 MDT Session Recording")
    st.markdown("<p style='color:#64748B;margin-top:-16px;margin-bottom:24px;'>Process 4.0 — Record multidisciplinary team decisions</p>", unsafe_allow_html=True)
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='sh'>Session Details</div>", unsafe_allow_html=True)
        mdt_id     = st.text_input("MDT Session ID",            placeholder="e.g. MDT-005")
        patient_id = st.text_input("Patient ID",                placeholder="e.g. P1001")
        report_id  = st.text_input("Report ID",                 placeholder="e.g. RPT-001")
        session_dt = st.date_input("Session Date",              value=date.today())
        doctor_ids = st.text_input("Doctor IDs (comma-separated)", placeholder="e.g. D001, D002")
    with col2:
        st.markdown("<div class='sh'>Clinical Decision</div>", unsafe_allow_html=True)
        notes    = st.text_area("Clinical Notes",  placeholder="Discussion summary...", height=100)
        decision = st.selectbox("Decision", ["Surgery","Chemotherapy","Radiotherapy","Immunotherapy","Systemic Therapy","Neoadjuvant Chemotherapy","Surgery + Adjuvant Chemo","Palliative Care","Active Surveillance","Pending"])
        treatment= st.text_area("Treatment Plan",  placeholder="Detailed treatment plan...", height=100)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✅ Record MDT Session"):
        if not all([mdt_id,patient_id,report_id,notes,treatment]): st.warning("Fill in all required fields.")
        else:
            doc_list = [d.strip() for d in doctor_ids.split(",") if d.strip()]
            r = post("/mdt/sessions", {"MDT_ID":mdt_id,"Date":datetime.combine(session_dt,datetime.min.time()).isoformat(),
                "patient_id":patient_id,"doctor_ids":doc_list,"report_id":report_id,"notes":notes,"decision":decision,"treatment_plan":treatment})
            if r and r.status_code==200: st.success(f"✅ MDT Session {mdt_id} recorded!")
            else: st.error(r.json().get("detail","Error") if r else "No response")
    st.divider()
    st.markdown("<div class='sh'>Recent MDT Sessions</div>", unsafe_allow_html=True)
    sess = get("/mdt/sessions")
    if sess:
        for s in sess[:5]:
            st.markdown(f"""<div class='card card-blue'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;'>
                    <div><div class='card-lbl'>{s.get("MDT_ID")} · Patient {s.get("patient_id")} · Report {s.get("report_id")}</div>
                    <div class='card-val'>{s.get("decision","—")}</div>
                    <div class='card-sub' style='margin-top:6px;'>{str(s.get("treatment_plan",""))[:110]}...</div></div>
                    <span class='badge-pend'>MDT Done</span>
                </div>
                <div style='margin-top:10px;padding-top:10px;border-top:1px solid #F1F5F9;color:#64748B;font-size:0.82rem;'>{str(s.get("notes",""))[:130]}...</div>
            </div>""", unsafe_allow_html=True)

def page_prognosis():
    st.markdown("# 📈 Prognostic Analysis")
    st.markdown("<p style='color:#64748B;margin-top:-16px;margin-bottom:24px;'>Process 5.0 — Risk assessment and clinical summary</p>", unsafe_allow_html=True)
    col1,col2 = st.columns([1,2])
    with col1:
        st.markdown("<div class='sh'>Patient Lookup</div>", unsafe_allow_html=True)
        p_id = st.text_input("Patient ID", placeholder="e.g. P1001")
        if st.button("🔍 Fetch Prognosis"):
            if not p_id: st.warning("Enter a Patient ID.")
            else:
                with st.spinner("Analysing..."):
                    data = get(f"/analysis/prognosis/{p_id}")
                if data:
                    with col2:
                        is_crit = data.get("is_critical", False)
                        badge   = "<span class='badge-crit'>CRITICAL</span>" if is_crit else "<span class='badge-ok'>ROUTINE</span>"
                        score   = data.get("automated_score", 0)
                        sc_cls  = "sc-red" if is_crit else "sc-green"
                        ac      = "red" if is_crit else "green"
                        st.markdown(f"""<div class='card card-{ac}'>
                            <div style='display:flex;justify-content:space-between;align-items:center;'>
                                <div><div class='card-lbl'>Patient Summary</div>
                                <div style='font-size:1.4rem;font-weight:700;color:#0F172A;margin:4px 0;'>{data.get("patient_name","—")}</div>
                                <div class='card-sub'>ID: {data.get("patient_id","—")}</div></div>
                                <div style='text-align:right;'>{badge}
                                <div class='{sc_cls}' style='margin-top:8px;'>{score:.1f}<span style='font-size:0.9rem;color:#64748B;font-weight:400;'>/25</span></div></div>
                            </div></div>""", unsafe_allow_html=True)
                        a,b,c = st.columns(3)
                        a.metric("Staging", data.get("staging_summary","N/A"))
                        b.metric("Risk Score", f"{score:.1f}/25")
                        c.metric("Status", "Critical" if is_crit else "Routine")
                        ac2 = "amber" if is_crit else "green"
                        st.markdown(f"""<div class='card card-blue' style='margin-top:16px;'>
                            <div class='card-lbl'>MDT Recommendation</div>
                            <div class='card-val' style='margin-top:4px;'>{data.get("mdt_recommendation","—")}</div></div>
                        <div class='card card-{ac2}'>
                            <div class='card-lbl'>MDT Decision</div>
                            <div class='card-val' style='margin-top:4px;'>{data.get("mdt_decision","—")}</div></div>""", unsafe_allow_html=True)
                else: st.error(f"Patient '{p_id}' not found.")
    st.divider()
    st.markdown("<div class='sh'>Patient Registry — Quick Access</div>", unsafe_allow_html=True)
    pts = get("/patients")
    if pts:
        df = pd.DataFrame(pts)
        cols = [c for c in ["Patient_ID","name","gender","Date_of_Birth"] if c in df.columns]
        st.dataframe(df[cols].rename(columns={"Patient_ID":"ID","name":"Name","gender":"Gender","Date_of_Birth":"DOB"}), use_container_width=True, hide_index=True)

def page_all_reports():
    st.markdown("# 📁 All Pathology Reports")
    reports = get("/pathology/reports/all")
    if not reports: st.info("No reports found."); return
    df = pd.DataFrame(reports)
    total  = len(df)
    crit   = int(df["is_critical"].sum()) if "is_critical" in df.columns else 0
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Reports", total)
    c2.metric("🚨 Critical",   crit)
    c3.metric("✅ Routine",    total-crit)
    st.markdown("<br>", unsafe_allow_html=True)
    for r in reports:
        m      = r.get("metrics",{}) or {}
        is_c   = r.get("is_critical", False)
        badge  = "<span class='badge-crit'>CRITICAL</span>" if is_c else "<span class='badge-ok'>ROUTINE</span>"
        sc_col = "#DC2626" if is_c else "#059669"
        ac     = "red" if is_c else "green"
        rmk    = f"<div class='card-sub' style='margin-top:8px;'>📝 {r.get('remarks','')}</div>" if r.get("remarks") else ""
        st.markdown(f"""<div class='card card-{ac}'>
            <div style='display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;'>
                <div style='flex:1;min-width:200px;'>
                    <div class='card-lbl'>{r.get("Report_ID","—")} · Patient {r.get("Patient_ID","—")}</div>
                    <div style='display:flex;gap:20px;margin-top:8px;flex-wrap:wrap;'>
                        <div><div class='card-lbl'>Tumor</div><div class='card-val'>{m.get("tumor","—")}</div></div>
                        <div><div class='card-lbl'>Node</div><div class='card-val'>{m.get("node","—")}</div></div>
                        <div><div class='card-lbl'>Metastasis</div><div class='card-val'>{m.get("metastasis","—")}</div></div>
                        <div><div class='card-lbl'>Grade</div><div class='card-val'>{m.get("grade","—")}</div></div>
                        <div><div class='card-lbl'>Priority</div><div class='card-val'>{r.get("priority","—")}</div></div>
                        <div><div class='card-lbl'>Status</div><div class='card-val'>{r.get("status","—")}</div></div>
                    </div>{rmk}
                </div>
                <div style='text-align:right;'>{badge}
                    <div style='color:{sc_col};font-weight:700;font-size:1.5rem;margin-top:6px;'>{r.get("automated_score",0)}<span style='font-size:0.85rem;color:#94A3B8;font-weight:400;'>/25</span></div>
                </div>
            </div></div>""", unsafe_allow_html=True)

def main():
    if st.session_state.token is None: login_page(); return
    menu = sidebar()
    if   "Overview"  in menu: page_overview()
    elif "Patients"  in menu: page_patients()
    elif "Lab Orders" in menu: page_orders()
    elif "Pathology" in menu: page_pathology()
    elif "MDT"       in menu: page_mdt()
    elif "Prognosis" in menu: page_prognosis()
    elif "All Reports" in menu: page_all_reports()

main()
