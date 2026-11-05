# 🔍 Digital Forensics Investigation System (DFIS)

**A Python-based Digital Forensics and Cybercrime Case Management System**

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![Database](https://img.shields.io/badge/Database-SQLite-blue)
![Status](https://img.shields.io/badge/Project-Academic%20Project-success)

## 📌 About the Project

The **Digital Forensics Investigation System (DFIS)** is a desktop-based application developed using Python to manage digital forensic investigations, cybercrime cases, digital evidence, chain of custody, and investigation reports.

The system provides a centralized platform for investigators to register cases, maintain evidence records, monitor investigation activities, and generate reports.

It aims to improve the organization, management, and tracking of digital forensic investigation processes.

## 🎯 Objectives

- Manage cybercrime investigation cases.
- Register and maintain digital evidence records.
- Track evidence collection and chain of custody.
- Monitor investigation progress and case status.
- Maintain investigator and user information.
- Generate investigation reports.
- Provide a centralized dashboard for investigation monitoring.

## ✨ Key Features

### 1. Dashboard
- Total registered cases.
- Active investigations.
- Critical cases.
- Total evidence records.
- Evidence tampering alerts.
- Case classification charts.
- Investigation status charts.
- Recent case and evidence activity.

### 2. Case Management
- Register new cybercrime cases.
- Maintain case details.
- Assign case priorities.
- Track investigation status.
- View registered cases.

### 3. Digital Evidence Management
- Register digital evidence.
- Maintain evidence identification details.
- Track evidence status.
- Associate evidence with investigation cases.

### 4. Chain of Custody
- Maintain evidence transfer records.
- Track evidence handling activities.
- Record custody information.
- Support evidence accountability.

### 5. Investigation Reports
- Maintain investigation report records.
- Organize case-related information.
- Generate reports for investigations.

### 6. User Management
- User authentication.
- Investigator account management.
- Access to system modules.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CustomTkinter | Desktop graphical interface |
| SQLite | Database management |
| Matplotlib | Dashboard charts and visualization |
| Tkinter | GUI framework |

## 📂 Project Structure

```text
Digital-Forensics-Investigation-System/
│
├── backend/
│   ├── __init__.py
│   ├── auth.py
│   ├── case_service.py
│   ├── custody_service.py
│   ├── database.py
│   ├── evidence_service.py
│   ├── report_service.py
│   └── user_service.py
│
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   ├── cases.py
│   ├── custody.py
│   ├── dashboard.py
│   ├── evidence.py
│   └── reports.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or above
- Visual Studio Code
- Git
- Windows 10/11 (or another supported Python desktop environment)

### Step 1: Clone the Repository

```bash
git clone https://github.com/shankar5377/Digital-Forensics-Investigation-System.git
```

### Step 2: Navigate to the Project

```bash
cd Digital-Forensics-Investigation-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate Virtual Environment

**Windows PowerShell:**

```powershell
.venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
python main.py
```

## 📊 Dashboard Overview

The dashboard provides an overview of investigation activities, including:

- Case statistics.
- Investigation priorities.
- Evidence records.
- Case classification.
- Investigation status.
- Recent activity.

## 🔐 Security Considerations

- Keep login credentials confidential.
- Restrict access to authorized investigators.
- Protect sensitive investigation records.
- Maintain evidence integrity using appropriate verification procedures.
- Preserve evidence handling records.
- Do not upload real confidential case data to a public repository.

**Note:** The application is an academic project and should not be considered a certified forensic evidence preservation platform without additional security validation.

## 🚀 Future Enhancements

- SHA-256 evidence integrity verification.
- Advanced forensic file analysis.
- Automated evidence metadata extraction.
- Advanced investigation analytics.
- Role-based access control.
- Improved PDF report generation.
- Audit logging and security monitoring.
- Cloud-based investigation management.

## 🎓 Project Information

**Project Name:** Digital Forensics Investigation System

**Project Type:** Academic / Software Development Project

**Domain:** Cybersecurity and Digital Forensics

**Developed Using:** Python

**IDE:** Visual Studio Code

## 👨‍💻 Developer

**Shankar**

GitHub: [@shankar5377](https://github.com/shankar5377)

Project Repository: [Digital-Forensics-Investigation-System](https://github.com/shankar5377/Digital-Forensics-Investigation-System)

## 📄 License

This project is developed for educational and academic purposes. Add a suitable open-source license if you intend to permit reuse and redistribution.

---

⭐ If you find this project useful, consider giving the repository a star!
