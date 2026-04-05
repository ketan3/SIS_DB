import requests
from faker import Faker
import random

fake = Faker('en_IN')
BASE_URL = "http://localhost:8000"

def post(endpoint, data):
    res = requests.post(f"{BASE_URL}{endpoint}", json=data)
    if res.status_code in [200, 201]:
        return res.json()
    else:
        print(f"❌ Error on {endpoint}: {res.status_code} - {res.text}")
        return None

# ─── 1. Lookups ───────────────────────────────────────────────────────

print("🌱 Seeding Lookups...")

categories = ["General", "OBC", "SC", "ST", "NT"]
category_ids = []
for name in categories:
    res = post("/categories", {"category_name": name})
    if res: category_ids.append(res["category_id"])

religions = ["Hindu", "Muslim", "Christian", "Buddhist", "Jain", "Sikh"]
religion_ids = []
for name in religions:
    res = post("/religions", {"religion_name": name})
    if res: religion_ids.append(res["religion_id"])

castes = ["Brahmin", "Maratha", "Kunbi", "Mali", "Teli", "Dhangar"]
caste_ids = []
for name in castes:
    res = post("/castes", {"caste_name": name})
    if res: caste_ids.append(res["caste_id"])

print(f"✅ Categories: {len(category_ids)}, Religions: {len(religion_ids)}, Castes: {len(caste_ids)}")

# ─── 2. Students ──────────────────────────────────────────────────────

print("🌱 Seeding Students...")

student_ids = []
for _ in range(10):
    data = {
        "first_name": fake.first_name(),
        "middle_name": fake.first_name(),
        "last_name": fake.last_name(),
        "date_of_birth": str(fake.date_of_birth(minimum_age=18, maximum_age=25)),
        "gender": random.choice(["Male", "Female"]),
        "blood_group": random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
        "mobile_number": fake.numerify("9#########"),
        "email_id": fake.unique.email(),
        "roll_number": fake.numerify("ROLL###"),
        "abc_id": fake.numerify("ABC#####"),
        "prn_number": fake.numerify("PRN#####"),
        "admission_date": str(fake.date_between(start_date="-2y", end_date="today")),
        "total_academic_fee": round(random.uniform(50000, 150000), 2),
        "total_submitted_fee": random.randint(20000, 80000),
        "total_pending_fee": random.randint(0, 50000),
        "scholarship_applied": random.choice([True, False]),
        "scholarship_amount": round(random.uniform(5000, 20000), 2),
        "apply_for_class": random.choice(["FY", "SY", "TY"]),
        "last_qualifying_exam": random.choice(["HSC", "SSC", "Diploma"]),
        "last_exam_board": random.choice(["Maharashtra Board", "CBSE", "ICSE"]),
    }
    res = post("/students/", data)
    if res:
        student_ids.append(res["student_id"])

print(f"✅ Students created: {len(student_ids)}")

# ─── 3. Demographics ─────────────────────────────────────────────────

print("🌱 Seeding Demographics...")
for sid in student_ids:
    post(f"/students/{sid}/demographics", {
        "category_id": random.choice(category_ids),
        "religion_id": random.choice(religion_ids),
        "caste_id": random.choice(caste_ids),
    })
print("✅ Demographics done")

# ─── 4. Family Details ───────────────────────────────────────────────

print("🌱 Seeding Family Details...")
for sid in student_ids:
    post(f"/students/{sid}/family", {
        "parent1_name": fake.name(),
        "parent1_phone": fake.numerify("9#########"),
        "parent1_occupation": fake.job(),
        "parent2_name": fake.name(),
        "parent2_phone": fake.numerify("9#########"),
        "parent2_occupation": fake.job(),
        "guardian_type": random.choice(["Father", "Mother", "Uncle", "Guardian"]),
        "guardian_name": fake.name(),
        "guardian_phone": fake.numerify("9#########"),
        "guardian_occupation": fake.job(),
    })
print("✅ Family details done")

# ─── 5. Addresses ────────────────────────────────────────────────────

print("🌱 Seeding Addresses...")
for sid in student_ids:
    for address_type in ["permanent", "current"]:
        addr = post("/addresses", {
            "line1": fake.street_address(),
            "line2": fake.street_name(),
            "city": fake.city(),
            "state": random.choice(["Maharashtra", "Gujarat", "Karnataka", "MP", "UP"]),
            "pincode": fake.numerify("4#####"),
            "country": "India",
        })
        if addr:
            post(f"/students/{sid}/addresses", {
                "address_id": addr["address_id"],
                "address_type": address_type,
            })
print("✅ Addresses done")

# ─── 6. Enrollments ──────────────────────────────────────────────────

print("🌱 Seeding Enrollments...")
departments = ["Computer Science", "Commerce", "Arts", "Science"]
programs = ["B.Sc", "B.Com", "BA", "BCA"]
for sid in student_ids:
    post("/enrollments/", {
        "student_id": sid,
        "department": random.choice(departments),
        "program": random.choice(programs),
        "class_name": random.choice(["FY", "SY", "TY"]),
        "division": random.choice(["A", "B", "C"]),
        "batch": random.choice(["2022-25", "2023-26", "2024-27"]),
    })
print("✅ Enrollments done")

# ─── 7. MOOC Courses ─────────────────────────────────────────────────

print("🌱 Seeding MOOC Courses...")
mooc_ids = []
courses = [
    {"platform": "Coursera", "course_name": "Python for Everybody", "credit_points": 4},
    {"platform": "NPTEL", "course_name": "Data Structures", "credit_points": 3},
    {"platform": "Swayam", "course_name": "Machine Learning", "credit_points": 4},
    {"platform": "edX", "course_name": "Web Development", "credit_points": 3},
    {"platform": "Udemy", "course_name": "Django REST Framework", "credit_points": 2},
]
for course in courses:
    res = post("/mooc-courses", course)
    if res: mooc_ids.append(res["mooc_course_id"])
print(f"✅ MOOC courses created: {len(mooc_ids)}")

# ─── 8. MOOC Enrollments ─────────────────────────────────────────────

print("🌱 Seeding MOOC Enrollments...")
for sid in student_ids:
    for mooc_id in random.sample(mooc_ids, k=2):
        post(f"/students/{sid}/mooc-enrollments", {
            "mooc_course_id": mooc_id,
            "grade": random.choice(["A", "B", "C", "O"]),
            "completion_date": str(fake.date_between(start_date="-1y", end_date="today")),
            "certificate_url": fake.url(),
        })
print("✅ MOOC enrollments done")

# ─── 9. Certificate Requests ─────────────────────────────────────────

print("🌱 Seeding Certificate Requests...")
cert_types = ["Bonafide", "Character", "Migration", "TC", "NOC"]
for sid in student_ids:
    post(f"/students/{sid}/certificates", {
        "certificate_type": random.choice(cert_types),
        "reason": fake.sentence(),
        "academic_year": random.choice(["2022-23", "2023-24", "2024-25"]),
    })
print("✅ Certificate requests done")

print("\n🎉 All done! Database seeded successfully.")