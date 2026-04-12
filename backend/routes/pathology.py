from fastapi import APIRouter, HTTPException, Depends
from models import TestReport, MDTSession, LabOrder
from database import reports_col, mdt_sessions_col, lab_orders_col
import logic
from auth import get_current_user

router = APIRouter(prefix="/pathology", tags=["Pathology"])


@router.post("/reports")
async def create_report(report: TestReport, current_user: str = Depends(get_current_user)):
    """Process 2.0 & 3.0 — Create and auto-score a new pathology report."""
    return logic.process_new_pathology_report(report)


@router.get("/reports/all")
async def get_all_reports(current_user: str = Depends(get_current_user)):
    """Retrieve last 50 pathology reports."""
    reports = list(reports_col.find().sort("Date", -1).limit(50))
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports


@router.get("/reports/{report_id}")
async def get_report(report_id: str, current_user: str = Depends(get_current_user)):
    """Retrieve a single report by ID."""
    report = reports_col.find_one({"Report_ID": report_id})
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report["_id"] = str(report["_id"])
    return report


@router.get("/reports/patient/{patient_id}")
async def get_reports_by_patient(patient_id: str, current_user: str = Depends(get_current_user)):
    """Retrieve all reports for a specific patient."""
    reports = list(reports_col.find({"Patient_ID": patient_id}).sort("Date", -1))
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports


@router.get("/critical")
async def get_critical_reports(current_user: str = Depends(get_current_user)):
    """Retrieve all critical (urgent MDT) reports."""
    reports = list(reports_col.find({"is_critical": True}).sort("Date", -1))
    for r in reports:
        r["_id"] = str(r["_id"])
    return reports
