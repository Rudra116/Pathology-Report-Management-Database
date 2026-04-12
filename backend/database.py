import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.module47_pathology

    # --- Collections ---
    patients_col     = db.patients
    doctors_col      = db.doctors
    lab_tests_col    = db.lab_tests
    lab_orders_col   = db.lab_orders
    reports_col      = db.pathology_reports
    mdt_sessions_col = db.mdt_sessions
    users_col        = db.users

    client.admin.command('ping')
    print("✅ M47: MongoDB connection successful")

except Exception as e:
    print(f"❌ M47: MongoDB connection failed: {e}")
    raise


def init_db_constraints():
    """Enforce unique indexes for all primary keys from ER diagram."""
    try:
        patients_col.create_index([("Patient_ID", ASCENDING)], unique=True)
        doctors_col.create_index([("Doctor_ID", ASCENDING)], unique=True)
        lab_tests_col.create_index([("Test_ID", ASCENDING)], unique=True)
        lab_orders_col.create_index([("Order_ID", ASCENDING)], unique=True)
        reports_col.create_index([("Report_ID", ASCENDING)], unique=True)
        mdt_sessions_col.create_index([("MDT_ID", ASCENDING)], unique=True)
        users_col.create_index([("username", ASCENDING)], unique=True)
        print("✅ M47: Database constraints and indexes initialized")
    except Exception as e:
        print(f"⚠️ M47: Error initializing constraints: {e}")
