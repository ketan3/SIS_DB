# College ERP: SIS Module (DB 2.0)

Welcome to the **Student Information System (SIS) Module** backend project.
This is a Code-First REST API implementation using **FastAPI**, **SQLAlchemy 2.0**, and **Alembic**.

---

## 🚀 Setting Up the Project Locally

If you are a team member taking over, follow these steps:

1. **Clone the Repository:**
   ```
   git clone https://github.com/ketan3/SIS_DB.git
   ```
2. **Create a Virtual Environment:**
   ```
   python -m venv .venv
   ```
3. **Activate Environment:**
   - Windows: `.venv\Scripts\activate`
   - Mac/Linux: `source .venv/bin/activate`
4. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
5. **Configure Database:**
   - Create a PostgreSQL database named `sis_db`.
   - Create a `.env` file in the root folder with:
     ```
     DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/sis_db
     ```
6. **Run Migrations:**
   ```
   alembic upgrade head
   ```
7. **Start the Server:**
   ```
   uvicorn app.main:app --reload
   ```
8. **View API Docs:** Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📂 Project Structure

```
SIS-DB2.0/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/                # Config & settings
│   ├── db/                  # Database engine & session
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── student.py       # StudentInformation, Demographics, FamilyDetails
│   │   ├── address.py       # Address, StudentAddress
│   │   ├── academic.py      # EnrollmentMapping, CertificateRequest
│   │   ├── mooc.py          # MoocCourse, StudentMoocEnrollment
│   │   ├── lookups.py       # Category, Religion, Caste
│   │   └── audit.py         # SIS Audit Log
│   ├── schemas/             # Pydantic request/response schemas
│   └── routers/             # API route handlers
│       ├── student.py
│       ├── address.py
│       ├── enrollment.py
│       ├── certificate.py
│       ├── mooc.py
│       └── lookup.py
├── alembic/                 # Database migration history
├── seed_data.py             # Script to seed initial lookup data
└── requirements.txt
```

---

## 📡 API Endpoints

### 👤 Student Profile (`/students`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students/` | Create a new student |
| GET | `/students/` | List all students |
| GET | `/students/{student_id}` | Get a student by ID |
| PATCH | `/students/{student_id}` | Update student details |
| DELETE | `/students/{student_id}` | **Soft-delete** (sets `is_active=False`) |
| POST | `/students/{student_id}/demographics` | Add demographics |
| GET | `/students/{student_id}/demographics` | Get demographics |
| PATCH | `/students/{student_id}/demographics` | Update demographics |
| POST | `/students/{student_id}/family` | Add family member |
| GET | `/students/{student_id}/family` | List family members |
| PATCH | `/students/{student_id}/family/{family_id}` | Update family member |
| DELETE | `/students/{student_id}/family/{family_id}` | Delete family member |

### 🏠 Addresses (`/addresses`, `/students/{id}/addresses`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/addresses` | Create an address record |
| PATCH | `/addresses/{address_id}` | Update an address record |
| POST | `/students/{student_id}/addresses` | Link an address to a student |
| GET | `/students/{student_id}/addresses` | Get all addresses for a student |
| PATCH | `/students/{student_id}/addresses/{id}` | Update a student's address link |
| DELETE | `/students/{student_id}/addresses/{id}` | Remove a student's address link |

### 📋 Enrollments (`/enrollments`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/enrollments/` | Create enrollment |
| GET | `/enrollments/` | List all enrollments |
| GET | `/enrollments/student/{student_id}` | Get enrollments by student |
| GET | `/enrollments/{enrollment_id}` | Get enrollment by ID |
| PATCH | `/enrollments/{enrollment_id}` | Update enrollment |
| DELETE | `/enrollments/{enrollment_id}` | Delete enrollment |

### 📜 Certificate Requests (`/students/{id}/certificates`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/students/{student_id}/certificates` | Submit certificate request |
| GET | `/students/{student_id}/certificates` | List all requests for a student |
| GET | `/students/{student_id}/certificates/{request_id}` | Get specific request |
| PATCH | `/students/{student_id}/certificates/{request_id}` | Update request / change **status** |
| DELETE | `/students/{student_id}/certificates/{request_id}` | Delete request |

> **Certificate Status Values:** `pending` → `approved` → `dispatched` (or `rejected`)

### 🎓 MOOC (`/mooc-courses`, `/students/{id}/mooc-enrollments`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/mooc-courses` | Add a MOOC course |
| GET | `/mooc-courses` | List all MOOC courses |
| GET | `/mooc-courses/{id}` | Get MOOC course by ID |
| PATCH | `/mooc-courses/{id}` | Update MOOC course |
| DELETE | `/mooc-courses/{id}` | Delete MOOC course |
| POST | `/students/{student_id}/mooc-enrollments` | Enroll student in MOOC |
| GET | `/students/{student_id}/mooc-enrollments` | List student MOOC enrollments |
| PATCH | `/students/{student_id}/mooc-enrollments/{mooc_id}` | Update enrollment |
| DELETE | `/students/{student_id}/mooc-enrollments/{mooc_id}` | Remove enrollment |

### 🔖 Lookups (`/categories`, `/religions`, `/castes`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/categories` | Add category |
| GET | `/categories` | List categories |
| PATCH | `/categories/{id}` | Update category |
| POST | `/religions` | Add religion |
| GET | `/religions` | List religions |
| PATCH | `/religions/{id}` | Update religion |
| POST | `/castes` | Add caste |
| GET | `/castes` | List castes |
| PATCH | `/castes/{id}` | Update caste |

> ⚠️ **Note:** DELETE is intentionally disabled for all lookup tables. These are FK-referenced master data — deleting them would corrupt `StudentDemographics` records.

---

## 🔑 Design Decisions

- **Soft-Delete for Students:** `DELETE /students/{id}` does NOT remove the record. It sets `is_active = False` to preserve enrollment history, certificates, and fee data.
- **No Standalone Address Listing:** `GET /addresses` is not exposed. Addresses are only meaningful in the context of a student — always use `/students/{id}/addresses`.
- **Lookup Data is Immutable (Delete-wise):** Categories, Religions, and Castes can only be created or updated, never deleted.
- **Certificate Status Workflow:** Every certificate request has a `status` field (`pending`, `approved`, `rejected`, `dispatched`) that admin staff update via PATCH.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework |
| **SQLAlchemy 2.0** | ORM (async) |
| **Alembic** | Database migrations |
| **asyncpg** | PostgreSQL async driver |
| **Pydantic v2** | Request/response validation |
| **PostgreSQL** | Primary database |

---

*Maintained by the SIS Team (M.Sc Computer Applications)*
