from fastapi import FastAPI
from app.routers import student, lookup, address, enrollment, mooc, certificate

def register_routers(app: FastAPI):
    app.include_router(student.router)
    app.include_router(lookup.router)
    app.include_router(address.router)
    app.include_router(enrollment.router)
    app.include_router(mooc.router)
    app.include_router(certificate.router)