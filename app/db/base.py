from app.db.base_class import Base
from app.models.lookups import Category, Religion, Caste
from app.models.student import StudentInformation, StudentDemographics, StudentFamilyDetails
from app.models.address import Address, StudentAddress
from app.models.academic import EnrollmentMapping, CertificateRequest
from app.models.mooc import MoocCourse, StudentMoocEnrollment
from app.models.audit import SisAuditLog
