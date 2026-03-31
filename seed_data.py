import asyncio
import random
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal
from app.models.lookups import Category, Religion, Caste
from app.models.student import StudentInformation, StudentDemographics, StudentFamilyDetails
from app.models.address import Address, StudentAddress

async def seed_data():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. Create Lookups
            categories = [Category(category_name="General"), Category(category_name="OBC"), Category(category_name="SC/ST")]
            religions = [Religion(religion_name="Hindu"), Religion(religion_name="Muslim"), Religion(religion_name="Christian")]
            castes = [Caste(caste_name="Brahmin"), Caste(caste_name="Maratha"), Caste(caste_name="None")]
            
            session.add_all(categories + religions + castes)
            await session.flush() # Sync with DB to get IDs

            # 2. Create Departments/Classes
            depts = ["Computer Science", "Animation", "Commerce"]
            sub_depts = {"Computer Science": ["Computer Application", "Computer Science"]}

            # 3. Create 10 Indian Students
            first_names = ["Amit", "Priya", "Rahul", "Sneha", "Vikram", "Anjali", "Suresh", "Pooja", "Deepak", "Neha"]
            last_names = ["Sharma", "Patil", "Verma", "Deshmukh", "Joshi", "Iyer", "Gupta", "Malhotra", "Kulkarni", "Reddy"]

            for i in range(10):
                # Random Scholarship Logic
                is_scholar = random.choice([True, False])
                amount = random.uniform(5000, 25000) if is_scholar else 0
                
                dept = random.choice(depts)
                sub_dept = random.choice(sub_depts[dept]) if dept == "Computer Science" else dept

                # Student Info
                student = StudentInformation(
                    first_name=first_names[i],
                    middle_name="Kumar" if i%2==0 else "Kumari",
                    last_name=last_names[i],
                    date_of_birth=date(2000, 1, 1),
                    gender="Male" if i%2==0 else "Female",
                    mobile_number=f"987654321{i}",
                    email_id=f"{first_names[i].lower()}{i}@example.com",
                    blood_group="O+",
                    roll_number=f"CS00{i}",
                    scholarship_applied=is_scholar,
                    scholarship_amount=amount,
                    apply_for_class=f"M.Sc {sub_dept}"
                )
                session.add(student)
                await session.flush()

                # Demographic (Foreign Key Test)
                demo = StudentDemographics(
                    student_id=student.student_id,
                    category_id=random.choice(categories).category_id,
                    religion_id=random.choice(religions).religion_id,
                    caste_id=random.choice(castes).caste_id
                )
                session.add(demo)

                # Address (Foreign Key Test)
                addr = Address(
                    line1=f"Flat {i+1}, Residency Road",
                    city="Mumbai" if i%2==0 else "Pune",
                    state="Maharashtra",
                    pincode="400001",
                    country="India"
                )
                session.add(addr)
                await session.flush()

                student_addr = StudentAddress(
                    student_id=student.student_id,
                    address_id=addr.address_id,
                    address_type="permanent"
                )
                session.add(student_addr)

                # Family Info (Foreign Key Test)
                family = StudentFamilyDetails(
                    student_id=student.student_id,
                    parent1_name=f"Mr. {last_names[i]}",
                    parent1_phone=f"999888777{i}",
                    parent1_occupation="Business"
                )
                session.add(family)

        print("Successfully seeded 10 Indian Student records! Check your database now.")

if __name__ == "__main__":
    asyncio.run(seed_data())
