# College ERP: SIS Module (DB 2.0)

Welcome to the **Student Information System (SIS) Module** backend project. This is a Code-First implementation using FastAPI, SQLAlchemy, and Alembic.

## 🚀 Setting Up the Project Locally

If you are a team member taking over, please follow these steps to get the project running on your machine:

1.  **Clone the Repository:** 
    `git clone <repository-link>`
2.  **Create a Virtual Environment:**
    `python -m venv .venv`
3.  **Activate Environment:**
    - Windows: `.venv\Scripts\activate`
    - Mac/Linux: `source .venv/bin/activate`
4.  **Install Dependencies:**
    `pip install -r requirements.txt`
5.  **Configure Database:**
    - Create a new PostgreSQL database named `sis_db`.
    - Create a `.env` file in the root folder.
    - Add this line: `DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/sis_db`
6.  **Run Migrations:**
    `alembic upgrade head`

## 📂 Project Structure
- **/app**: Core logic, database setup, and all 13 SQLAlchemy models.
- **/alembic**: Database migration history and version control.
- **SIS_API_GUIDE.html**: A complete guide on how to call APIs from other modules.

## 🛠️ Tech Stack
- **FastAPI**: Modern, high-performance web framework.
- **SQLAlchemy 2.0**: Python SQL Toolkit and Object Relational Mapper.
- **Alembic**: Database migrations tool.
- **asyncpg**: Database driver for PostgreSQL.

---
*Maintained by the SIS Team (M.Sc Computer Applications)*
