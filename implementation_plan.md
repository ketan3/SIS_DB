# Fix Problematic APIs in SIS-DB2.0

Fix 7 identified issues across routers, models, and schemas — all low-risk, surgical changes.

## Proposed Changes

---

### 1. Address Router — Remove Pointless Standalone Endpoints

#### [MODIFY] [address.py](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/routers/address.py)

Remove these 3 endpoints that expose raw addresses without any student context:
- `GET /addresses` — meaningless, no student context
- `GET /addresses/{address_id}` — no way to know whose address it is
- `DELETE /addresses/{address_id}` — dangerous, can break other students' links

Keep only: `POST /addresses`, `PATCH /addresses/{id}`, and all `/students/{id}/addresses` endpoints.

---

### 2. Lookup Router — Remove Delete Endpoints for Master Data

#### [MODIFY] [lookup.py](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/routers/lookup.py)

Remove `DELETE` for categories, religions, and castes. These are FK-referenced master data — deleting them breaks `StudentDemographics` records.

Affected deletions:
- `DELETE /categories/{category_id}`
- `DELETE /religions/{religion_id}`
- `DELETE /castes/{caste_id}`

---

### 3. Student Router — Soft-Delete + Fix Demographics Schema

#### [MODIFY] [student.py (router)](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/routers/student.py)

- **`DELETE /students/{student_id}`** → Change to soft-delete: set `is_active = False` instead of removing the row.
- **`PATCH /{student_id}/demographics`** → Switch from `DemographicsCreate` to `DemographicsUpdate` (all-optional) schema.

#### [MODIFY] [student.py (model)](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/models/student.py)

- Add `is_active: Mapped[bool]` field (default `True`) to `StudentInformation`.

#### [MODIFY] [student.py (schema)](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/schemas/student.py)

- Add `DemographicsUpdate` class with all-optional fields.
- Add `is_active` to `StudentResponse`.

---

### 4. Enrollment Router — Fix Route Order Bug

#### [MODIFY] [enrollment.py](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/routers/enrollment.py)

Move `GET /enrollments/student/{student_id}` **above** `GET /enrollments/{enrollment_id}` to prevent FastAPI matching `"student"` as an int.

---

### 5. Certificate Model & Schema — Add Status Field

#### [MODIFY] [academic.py (model)](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/models/academic.py)

Add `status` field to `CertificateRequest` with values: `pending`, `approved`, `rejected`, `dispatched`. Default: `pending`.

#### [MODIFY] [certificate.py (schema)](file:///e:/Ketan/SIS-API2/SIS-DB2.0/app/schemas/certificate.py)

- Add `status: Optional[str]` to `CertificateUpdate`.
- Add `status: str` to `CertificateResponse`.

---

## Verification Plan

- Run the dev server (`uvicorn`) and verify no import errors.
- Check FastAPI `/docs` to confirm removed endpoints are gone and new `status` field appears.
- Generate an Alembic migration for the two model changes (`is_active` on student, `status` on certificate).

> [!IMPORTANT]
> Model changes (`is_active` on `StudentInformation` and `status` on `CertificateRequest`) require a **new Alembic migration** (`alembic revision --autogenerate`). I'll generate this as part of the fix.
