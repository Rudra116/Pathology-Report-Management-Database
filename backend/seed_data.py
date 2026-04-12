"""
M47 Pathology Report Management System — Dummy Data Seeder
Run this ONCE before launching the app:
    cd backend
    python seed_data.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import (
    users_col, patients_col, doctors_col, lab_tests_col,
    lab_orders_col, reports_col, mdt_sessions_col
)
from auth import hash_password
from datetime import datetime

print("🌱 Seeding M47 database with dummy data...")


# ─── CLEAR OLD DATA ───────────────────────────────────────────────────────────
for col in [users_col, patients_col, doctors_col, lab_tests_col,
            lab_orders_col, reports_col, mdt_sessions_col]:
    col.delete_many({})
print("🗑️  Old data cleared.")


# ─── USERS ────────────────────────────────────────────────────────────────────
users = [
    {"username": "admin",    "hashed_password": hash_password("admin123"),   "role": "Admin"},
    {"username": "drsmith",  "hashed_password": hash_password("doctor123"),  "role": "Doctor"},
    {"username": "drpatel",  "hashed_password": hash_password("doctor123"),  "role": "Doctor"},
    {"username": "labtech1", "hashed_password": hash_password("lab123"),     "role": "Technician"},
]
users_col.insert_many(users)
print(f"✅ {len(users)} users seeded  |  Login: admin / admin123  or  drsmith / doctor123")


# ─── DOCTORS ──────────────────────────────────────────────────────────────────
doctors = [
    {"Doctor_ID": "D001", "name": "Dr. Arjun Sharma",    "specialization": "Oncology"},
    {"Doctor_ID": "D002", "name": "Dr. Priya Patel",     "specialization": "Pathology"},
    {"Doctor_ID": "D003", "name": "Dr. Rohit Mehta",     "specialization": "Radiology"},
    {"Doctor_ID": "D004", "name": "Dr. Sana Khan",       "specialization": "Surgery"},
    {"Doctor_ID": "D005", "name": "Dr. Vikram Nair",     "specialization": "Medical Oncology"},
]
doctors_col.insert_many(doctors)
print(f"✅ {len(doctors)} doctors seeded")


# ─── PATIENTS ─────────────────────────────────────────────────────────────────
patients = [
    {"Patient_ID": "P1001", "name": "Rajesh Kumar",      "Date_of_Birth": "1965-03-15", "gender": "Male"},
    {"Patient_ID": "P1002", "name": "Sunita Devi",       "Date_of_Birth": "1972-07-22", "gender": "Female"},
    {"Patient_ID": "P1003", "name": "Mohan Lal",         "Date_of_Birth": "1958-11-08", "gender": "Male"},
    {"Patient_ID": "P1004", "name": "Anita Singh",       "Date_of_Birth": "1980-01-30", "gender": "Female"},
    {"Patient_ID": "P1005", "name": "Deepak Verma",      "Date_of_Birth": "1945-09-12", "gender": "Male"},
    {"Patient_ID": "P1006", "name": "Kavitha Rao",       "Date_of_Birth": "1968-05-19", "gender": "Female"},
    {"Patient_ID": "P1007", "name": "Suresh Babu",       "Date_of_Birth": "1975-12-03", "gender": "Male"},
    {"Patient_ID": "P1008", "name": "Meena Pillai",      "Date_of_Birth": "1990-08-27", "gender": "Female"},
    {"Patient_ID": "P1009", "name": "Arun Krishnan",     "Date_of_Birth": "1952-04-14", "gender": "Male"},
    {"Patient_ID": "P1010", "name": "Fatima Begum",      "Date_of_Birth": "1963-06-01", "gender": "Female"},
]
patients_col.insert_many(patients)
print(f"✅ {len(patients)} patients seeded")


# ─── LAB TESTS ────────────────────────────────────────────────────────────────
lab_tests = [
    {"Test_ID": "T001", "name": "Biopsy - Core Needle",      "category": "Histopathology"},
    {"Test_ID": "T002", "name": "Fine Needle Aspiration",     "category": "Cytology"},
    {"Test_ID": "T003", "name": "Immunohistochemistry",       "category": "Molecular"},
    {"Test_ID": "T004", "name": "Flow Cytometry",             "category": "Hematology"},
    {"Test_ID": "T047", "name": "TNM Cancer Staging Panel",   "category": "Oncology"},
]
lab_tests_col.insert_many(lab_tests)
print(f"✅ {len(lab_tests)} lab tests seeded")


# ─── LAB ORDERS ───────────────────────────────────────────────────────────────
lab_orders = [
    {"Order_ID": "LO-001", "patient_id": "P1001", "doctor_id": "D001", "date": "2024-01-10", "status": "Completed"},
    {"Order_ID": "LO-002", "patient_id": "P1002", "doctor_id": "D002", "date": "2024-01-15", "status": "Completed"},
    {"Order_ID": "LO-003", "patient_id": "P1003", "doctor_id": "D001", "date": "2024-01-18", "status": "Completed"},
    {"Order_ID": "LO-004", "patient_id": "P1004", "doctor_id": "D003", "date": "2024-02-05", "status": "Completed"},
    {"Order_ID": "LO-005", "patient_id": "P1005", "doctor_id": "D004", "date": "2024-02-12", "status": "Completed"},
    {"Order_ID": "LO-006", "patient_id": "P1006", "doctor_id": "D001", "date": "2024-02-20", "status": "Completed"},
    {"Order_ID": "LO-007", "patient_id": "P1007", "doctor_id": "D005", "date": "2024-03-01", "status": "Pending"},
    {"Order_ID": "LO-008", "patient_id": "P1008", "doctor_id": "D002", "date": "2024-03-08", "status": "Completed"},
    {"Order_ID": "LO-009", "patient_id": "P1009", "doctor_id": "D001", "date": "2024-03-15", "status": "Completed"},
    {"Order_ID": "LO-010", "patient_id": "P1010", "doctor_id": "D003", "date": "2024-03-22", "status": "Pending"},
]
lab_orders_col.insert_many(lab_orders)
print(f"✅ {len(lab_orders)} lab orders seeded")


# ─── PATHOLOGY REPORTS ────────────────────────────────────────────────────────
reports = [
    {
        "Report_ID": "RPT-001", "Order_ID": "LO-001", "Patient_ID": "P1001",
        "test_id": "T047", "Date": datetime(2024, 1, 12), "status": "Final",
        "priority": "Urgent", "remarks": "Large mass detected in right lung",
        "metrics": {"Metric_ID": "M-001", "tumor": "T4", "node": "N2", "metastasis": "M1", "result": "Biopsy", "grade": "High"},
        "automated_score": 22.0, "is_critical": True, "initial_implication": "URGENT MDT REFERRAL REQUIRED"
    },
    {
        "Report_ID": "RPT-002", "Order_ID": "LO-002", "Patient_ID": "P1002",
        "test_id": "T001", "Date": datetime(2024, 1, 17), "status": "Final",
        "priority": "Routine", "remarks": "Small localized nodule, margins clear",
        "metrics": {"Metric_ID": "M-002", "tumor": "T1", "node": "N0", "metastasis": "M0", "result": "Biopsy", "grade": "G1"},
        "automated_score": 0.0, "is_critical": False, "initial_implication": "Routine Follow-up Recommended"
    },
    {
        "Report_ID": "RPT-003", "Order_ID": "LO-003", "Patient_ID": "P1003",
        "test_id": "T047", "Date": datetime(2024, 1, 20), "status": "Final",
        "priority": "High", "remarks": "Lymph node involvement confirmed",
        "metrics": {"Metric_ID": "M-003", "tumor": "T3", "node": "N1", "metastasis": "M0", "result": "Biopsy", "grade": "G3"},
        "automated_score": 15.0, "is_critical": True, "initial_implication": "URGENT MDT REFERRAL REQUIRED"
    },
    {
        "Report_ID": "RPT-004", "Order_ID": "LO-004", "Patient_ID": "P1004",
        "test_id": "T002", "Date": datetime(2024, 2, 7), "status": "Final",
        "priority": "Routine", "remarks": "Benign tissue, no malignancy",
        "metrics": {"Metric_ID": "M-004", "tumor": "T1", "node": "N0", "metastasis": "M0", "result": "FNA", "grade": "G1"},
        "automated_score": 0.0, "is_critical": False, "initial_implication": "Routine Follow-up Recommended"
    },
    {
        "Report_ID": "RPT-005", "Order_ID": "LO-005", "Patient_ID": "P1005",
        "test_id": "T047", "Date": datetime(2024, 2, 14), "status": "Final",
        "priority": "Urgent", "remarks": "Distant metastasis to liver confirmed",
        "metrics": {"Metric_ID": "M-005", "tumor": "T4", "node": "N2", "metastasis": "M1", "result": "Biopsy", "grade": "High"},
        "automated_score": 22.0, "is_critical": True, "initial_implication": "URGENT MDT REFERRAL REQUIRED"
    },
    {
        "Report_ID": "RPT-006", "Order_ID": "LO-006", "Patient_ID": "P1006",
        "test_id": "T003", "Date": datetime(2024, 2, 22), "status": "Preliminary",
        "priority": "High", "remarks": "IHC markers positive for ER/PR",
        "metrics": {"Metric_ID": "M-006", "tumor": "T2", "node": "N1", "metastasis": "M0", "result": "IHC", "grade": "G2"},
        "automated_score": 3.0, "is_critical": False, "initial_implication": "Routine Follow-up Recommended"
    },
    {
        "Report_ID": "RPT-007", "Order_ID": "LO-008", "Patient_ID": "P1008",
        "test_id": "T047", "Date": datetime(2024, 3, 10), "status": "Final",
        "priority": "High", "remarks": "Aggressive tumor grade, rapid growth",
        "metrics": {"Metric_ID": "M-007", "tumor": "T3", "node": "N2", "metastasis": "M0", "result": "Biopsy", "grade": "High"},
        "automated_score": 15.0, "is_critical": True, "initial_implication": "URGENT MDT REFERRAL REQUIRED"
    },
    {
        "Report_ID": "RPT-008", "Order_ID": "LO-009", "Patient_ID": "P1009",
        "test_id": "T001", "Date": datetime(2024, 3, 17), "status": "Final",
        "priority": "Routine", "remarks": "Follow-up biopsy, stable",
        "metrics": {"Metric_ID": "M-008", "tumor": "T2", "node": "N0", "metastasis": "M0", "result": "Biopsy", "grade": "G2"},
        "automated_score": 0.0, "is_critical": False, "initial_implication": "Routine Follow-up Recommended"
    },
]
reports_col.insert_many(reports)
print(f"✅ {len(reports)} pathology reports seeded")


# ─── MDT SESSIONS ─────────────────────────────────────────────────────────────
mdt_sessions = [
    {
        "MDT_ID": "MDT-001", "Date": datetime(2024, 1, 25), "patient_id": "P1001",
        "doctor_ids": ["D001", "D002", "D004"],
        "report_id": "RPT-001",
        "notes": "Patient presents with stage IV NSCLC. PET scan confirms liver and bone metastases. ECOG performance status 2.",
        "decision": "Systemic Therapy",
        "treatment_plan": "Initiate platinum-based chemotherapy (Carboplatin + Paclitaxel) with concurrent immunotherapy (Pembrolizumab). Monthly monitoring."
    },
    {
        "MDT_ID": "MDT-002", "Date": datetime(2024, 2, 5), "patient_id": "P1003",
        "doctor_ids": ["D001", "D003", "D005"],
        "report_id": "RPT-003",
        "notes": "Stage IIIA colorectal cancer. CT shows N1 nodal involvement. Surgery feasible.",
        "decision": "Surgery + Adjuvant Chemo",
        "treatment_plan": "Laparoscopic colectomy followed by 6 cycles of FOLFOX chemotherapy. Re-staging CT at 3 months."
    },
    {
        "MDT_ID": "MDT-003", "Date": datetime(2024, 2, 28), "patient_id": "P1005",
        "doctor_ids": ["D001", "D002", "D004", "D005"],
        "report_id": "RPT-005",
        "notes": "Metastatic gastric cancer. ECOG 3. Palliative intent discussed with family.",
        "decision": "Palliative Care",
        "treatment_plan": "Best supportive care with palliative chemotherapy (Capecitabine). Oncology palliative team referral. Weekly symptom review."
    },
    {
        "MDT_ID": "MDT-004", "Date": datetime(2024, 3, 20), "patient_id": "P1008",
        "doctor_ids": ["D001", "D002", "D003"],
        "report_id": "RPT-007",
        "notes": "Triple-negative breast cancer T3N2. HER2 negative. Neoadjuvant approach preferred.",
        "decision": "Neoadjuvant Chemotherapy",
        "treatment_plan": "Neoadjuvant AC-T (Adriamycin + Cyclophosphamide, then Taxol) followed by surgical reassessment. Genetic counselling arranged."
    },
]
mdt_sessions_col.insert_many(mdt_sessions)
print(f"✅ {len(mdt_sessions)} MDT sessions seeded")

print("\n" + "="*60)
print("🎉 M47 Database seeding complete!")
print("="*60)
print("\n📋 LOGIN CREDENTIALS:")
print("   Username: admin      | Password: admin123    | Role: Admin")
print("   Username: drsmith    | Password: doctor123   | Role: Doctor")
print("   Username: drpatel    | Password: doctor123   | Role: Doctor")
print("   Username: labtech1   | Password: lab123      | Role: Technician")
print("\n🚀 To start backend:  uvicorn main:app --reload")
print("🖥️  To start frontend: streamlit run ../frontend/dashboard.py")
print("="*60)
