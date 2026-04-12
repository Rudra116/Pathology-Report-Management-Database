from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date


# --- Authentication Models ---
class User(BaseModel):
    username: str
    role: str  # Admin, Doctor, Technician

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# --- Entity Models (ER Diagram) ---
class Patient(BaseModel):
    patient_id: str = Field(..., alias="Patient_ID")
    name: str
    dob: date = Field(..., alias="Date_of_Birth")
    gender: str

    class Config:
        populate_by_name = True

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class Doctor(BaseModel):
    doctor_id: str = Field(..., alias="Doctor_ID")
    name: str
    specialization: str

    class Config:
        populate_by_name = True


class LabTest(BaseModel):
    test_id: str = Field(..., alias="Test_ID")
    name: str
    category: str

    class Config:
        populate_by_name = True


class LabOrder(BaseModel):
    order_id: str = Field(..., alias="Order_ID")
    patient_id: str
    doctor_id: str
    date: datetime = Field(default_factory=datetime.now)
    status: str

    class Config:
        populate_by_name = True


class CancerMetrics(BaseModel):
    metric_id: str = Field(..., alias="Metric_ID")
    tumor: str      # T1–T4
    node: str       # N0–N2
    metastasis: str # M0–M1
    result: str     # e.g. Biopsy
    grade: str      # G1, G2, G3, High

    class Config:
        populate_by_name = True


class TestReport(BaseModel):
    report_id: str = Field(..., alias="Report_ID")
    order_id: str
    patient_id: str = Field(..., alias="Patient_ID")
    test_id: str
    report_date: datetime = Field(default_factory=datetime.now, alias="Date")
    status: str
    remarks: Optional[str] = None
    priority: str
    metrics: Optional[CancerMetrics] = None

    class Config:
        populate_by_name = True


class MDTSession(BaseModel):
    mdt_id: str = Field(..., alias="MDT_ID")
    session_date: datetime = Field(..., alias="Date")
    patient_id: str
    doctor_ids: List[str]
    report_id: str
    notes: str
    decision: str
    treatment_plan: str

    class Config:
        populate_by_name = True
