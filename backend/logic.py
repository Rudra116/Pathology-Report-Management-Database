from fastapi import HTTPException
from database import patients_col, reports_col, mdt_sessions_col, lab_orders_col
from models import TestReport, MDTSession


# --- PROCESS 3.0: Cancer Staging & Grading ---
def calculate_prognosis(report: TestReport):
    """
    Automated TNM staging score.
    Returns (score, is_critical, implication)
    """
    score = 0.0
    is_critical = False
    metrics = report.metrics

    if not metrics:
        return 0.0, False, "No Metrics Provided"

    # Metastasis check (M stage)
    if metrics.metastasis != "M0":
        score += 10.0
        is_critical = True

    # Tumor size check (T stage)
    if metrics.tumor in ["T3", "T4"]:
        score += 5.0
        is_critical = True

    # Grade check
    if metrics.grade in ["High", "G3"]:
        score += 7.0
        is_critical = True

    # Node involvement
    if metrics.node in ["N1", "N2"]:
        score += 3.0

    implication = "URGENT MDT REFERRAL REQUIRED" if is_critical else "Routine Follow-up Recommended"
    return score, is_critical, implication


# --- PROCESS 2.0: Report Management ---
def process_new_pathology_report(report: TestReport):
    """Store a new pathology report and compute its automated score."""
    # Validate that the Lab Order exists
    order = lab_orders_col.find_one({"Order_ID": report.order_id})
    if not order:
        raise HTTPException(status_code=404, detail=f"Lab Order '{report.order_id}' not found. Please create the order first.")

    score, is_critical, implication = calculate_prognosis(report)

    report_dict = report.dict(by_alias=True)
    report_dict["automated_score"] = score
    report_dict["is_critical"] = is_critical
    report_dict["initial_implication"] = implication

    try:
        reports_col.insert_one(report_dict)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Report already exists or DB error: {str(e)}")

    return {
        "status": "Report Stored Successfully",
        "report_id": report.report_id,
        "is_critical": is_critical,
        "automated_score": score,
        "implication": implication
    }


# --- PROCESS 4.0: MDT Meeting Module ---
def record_mdt_discussion(session: MDTSession):
    """Record an MDT session linked to a pathology report."""
    report = reports_col.find_one({"Report_ID": session.report_id})
    if not report:
        raise HTTPException(status_code=404, detail=f"Report '{session.report_id}' not found.")

    try:
        mdt_sessions_col.insert_one(session.dict(by_alias=True))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"MDT session error: {str(e)}")

    return {"status": "MDT Decision Recorded", "mdt_id": session.mdt_id}


# --- PROCESS 5.0: Prognostic & Treatment Analysis ---
def get_final_prognostic_summary(patient_id: str):
    """Aggregate patient data, latest report, and MDT recommendation."""
    patient = patients_col.find_one({"Patient_ID": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient '{patient_id}' not found.")

    latest_report = reports_col.find_one(
        {"Patient_ID": patient_id},
        sort=[("Date", -1)]
    )
    latest_mdt = mdt_sessions_col.find_one(
        {"patient_id": patient_id},
        sort=[("Date", -1)]
    )

    staging_summary = "N/A"
    is_critical = False
    score = 0.0

    if latest_report:
        metrics = latest_report.get("metrics", {})
        if metrics:
            staging_summary = (
                f"T:{metrics.get('tumor','?')} "
                f"N:{metrics.get('node','?')} "
                f"M:{metrics.get('metastasis','?')} "
                f"Grade:{metrics.get('grade','?')}"
            )
        is_critical = latest_report.get("is_critical", False)
        score = latest_report.get("automated_score", 0.0)

    return {
        "patient_name": patient.get("name", "Unknown"),
        "patient_id": patient_id,
        "staging_summary": staging_summary,
        "automated_score": score,
        "is_critical": is_critical,
        "mdt_recommendation": latest_mdt.get("treatment_plan", "Pending MDT Review") if latest_mdt else "Pending MDT Review",
        "mdt_decision": latest_mdt.get("decision", "N/A") if latest_mdt else "N/A",
        "final_status": "Prognostic analysis complete"
    }
