from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from models import Patient, LabOrder, TestReport, MDTSession, Token, Doctor, LabTest
from datetime import date, datetime
from database import (
    init_db_constraints, users_col, patients_col,
    lab_orders_col, doctors_col, lab_tests_col, mdt_sessions_col, reports_col
)
import logic
import auth
from routes import pathology

app = FastAPI(
    title="M47 Pathology Report Management System",
    description="Backend API for oncology pathology report management with TNM staging, MDT sessions, and prognostic analysis.",
    version="1.0.0"
)

# CORS — allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pathology.router)


@app.on_event("startup")
async def startup_event():
    init_db_constraints()


# ─── PROCESS 1.0: USER AUTHENTICATION ────────────────────────────────────────

@app.post("/auth/register", tags=["Authentication"])
async def register(username: str, password: str, role: str = "Doctor"):
    if users_col.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.hash_password(password)
    users_col.insert_one({"username": username, "hashed_password": hashed_password, "role": role})
    return {"message": f"User '{username}' created successfully with role '{role}'"}


@app.post("/auth/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_col.find_one({"username": form_data.username})
    if not user or not auth.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# ─── PATIENTS ─────────────────────────────────────────────────────────────────

@app.post("/patients", tags=["Data Entry"])
async def register_patient(patient: Patient, current_user: str = Depends(auth.get_current_user)):
    try:
        patient_data = patient.dict(by_alias=True)
        if isinstance(patient_data.get("Date_of_Birth"), (date, datetime)):
            patient_data["Date_of_Birth"] = patient_data["Date_of_Birth"].isoformat()
        patients_col.insert_one(patient_data)
        return {"message": f"Patient '{patient.name}' registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/patients", tags=["Data Entry"])
async def get_all_patients(current_user: str = Depends(auth.get_current_user)):
    patients = list(patients_col.find().limit(100))
    for p in patients:
        p["_id"] = str(p["_id"])
    return patients


@app.get("/patients/{patient_id}", tags=["Data Entry"])
async def get_patient(patient_id: str, current_user: str = Depends(auth.get_current_user)):
    patient = patients_col.find_one({"Patient_ID": patient_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    patient["_id"] = str(patient["_id"])
    return patient


# ─── DOCTORS ──────────────────────────────────────────────────────────────────

@app.post("/doctors", tags=["Data Entry"])
async def register_doctor(doctor: Doctor, current_user: str = Depends(auth.get_current_user)):
    try:
        doctors_col.insert_one(doctor.dict(by_alias=True))
        return {"message": f"Doctor '{doctor.name}' registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/doctors", tags=["Data Entry"])
async def get_all_doctors(current_user: str = Depends(auth.get_current_user)):
    doctors = list(doctors_col.find().limit(100))
    for d in doctors:
        d["_id"] = str(d["_id"])
    return doctors


# ─── LAB ORDERS ───────────────────────────────────────────────────────────────

@app.post("/orders", tags=["Data Entry"])
async def create_lab_order(order: LabOrder, current_user: str = Depends(auth.get_current_user)):
    try:
        order_data = order.dict(by_alias=True)
        if isinstance(order_data.get("date"), datetime):
            order_data["date"] = order_data["date"].isoformat()
        lab_orders_col.insert_one(order_data)
        return {"message": f"Lab Order '{order.order_id}' created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/orders", tags=["Data Entry"])
async def get_all_orders(current_user: str = Depends(auth.get_current_user)):
    orders = list(lab_orders_col.find().limit(100))
    for o in orders:
        o["_id"] = str(o["_id"])
    return orders


# ─── PROCESS 2.0 & 3.0: REPORT MANAGEMENT ────────────────────────────────────

@app.post("/pathology/reports", tags=["Report Management"])
async def create_pathology_report(report: TestReport, current_user: str = Depends(auth.get_current_user)):
    return logic.process_new_pathology_report(report)


# ─── PROCESS 4.0: MDT MEETING MODULE ─────────────────────────────────────────

@app.post("/mdt/sessions", tags=["MDT Meeting"])
async def record_mdt_session(session: MDTSession, current_user: str = Depends(auth.get_current_user)):
    return logic.record_mdt_discussion(session)


@app.get("/mdt/sessions", tags=["MDT Meeting"])
async def get_all_mdt_sessions(current_user: str = Depends(auth.get_current_user)):
    sessions = list(mdt_sessions_col.find().sort("Date", -1).limit(50))
    for s in sessions:
        s["_id"] = str(s["_id"])
    return sessions


# ─── PROCESS 5.0: ANALYSIS ───────────────────────────────────────────────────

@app.get("/analysis/prognosis/{patient_id}", tags=["Analysis"])
async def get_patient_prognosis(patient_id: str, current_user: str = Depends(auth.get_current_user)):
    return logic.get_final_prognostic_summary(patient_id)


@app.get("/analysis/stats", tags=["Analysis"])
async def get_dashboard_stats(current_user: str = Depends(auth.get_current_user)):
    """Summary stats for the dashboard overview."""
    total_patients = patients_col.count_documents({})
    total_reports = reports_col.count_documents({})
    critical_reports = reports_col.count_documents({"is_critical": True})
    pending_mdt = mdt_sessions_col.count_documents({"decision": "Pending"})
    return {
        "total_patients": total_patients,
        "total_reports": total_reports,
        "critical_reports": critical_reports,
        "pending_mdt": pending_mdt
    }


@app.get("/", tags=["Health"])
async def root():
    return {"message": "M47 Pathology API is running", "version": "1.0.0"}
