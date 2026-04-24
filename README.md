# M47 Pathology Report Management System

## Live Project Link
https://pathology-report-management-database-f2sgzjvasnncfsqshqupo4.streamlit.app

## Project Structure
```
project/
├── backend/
│   ├── main.py          — FastAPI app, all endpoints
│   ├── models.py        — Pydantic models (ER diagram entities)
│   ├── database.py      — MongoDB connection & collections
│   ├── auth.py          — JWT authentication
│   ├── logic.py         — Business logic (TNM scoring, prognosis)
│   ├── seed_data.py     — Dummy data seeder (run once)
│   ├── .env             — Environment variables
│   └── routes/
│       ├── __init__.py
│       └── pathology.py — Pathology-specific routes
├── frontend/
│   └── dashboard.py     — Streamlit UI
└── requirements.txt
```

## ⚙️ Setup (5 minutes)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Make sure MongoDB is running
```bash
# macOS
brew services start mongodb-community

# Ubuntu/Linux
sudo systemctl start mongod

# Windows — start MongoDB service from Services panel
```

### 3. Seed the database with dummy data
```bash
cd backend
python seed_data.py
```

### 4. Start the backend API
```bash
cd backend
uvicorn main:app --reload
# API runs at http://127.0.0.1:8000
# Swagger docs at http://127.0.0.1:8000/docs
```

### 5. Start the frontend (new terminal)
```bash
streamlit run frontend/dashboard.py
# Dashboard at http://localhost:8501
```

## 🔑 Login Credentials (Dummy Data)

| Username   | Password    | Role        |
|------------|-------------|-------------|
| admin      | admin123    | Admin       |
| drsmith    | doctor123   | Doctor      |
| drpatel    | doctor123   | Doctor      |
| labtech1   | lab123      | Technician  |

## 📋 Pre-loaded Dummy Data

- **10 patients** (P1001–P1010)
- **5 doctors** (D001–D005)
- **5 lab tests** including TNM Staging Panel
- **10 lab orders** (LO-001–LO-010)
- **8 pathology reports** (mix of critical and routine)
- **4 MDT sessions** with treatment plans

## 🏥 System Processes (DFD)

| Process | Description |
|---------|-------------|
| 1.0 | User Authentication (JWT) |
| 2.0 | Report Management (Create/Store) |
| 3.0 | Cancer Staging, TNM Grading (Auto-score) |
| 4.0 | MDT Meeting Module (Record decisions) |
| 5.0 | Prognostic & Treatment Analysis |

## 📊 TNM Auto-Scoring Logic

| Factor | Points |
|--------|--------|
| Metastasis M1 | +10 |
| Grade G3 or High | +7 |
| Tumor T3 or T4 | +5 |
| Node N1 or N2 | +3 |
| **Score > 7** | → **CRITICAL (MDT Referral)** |
