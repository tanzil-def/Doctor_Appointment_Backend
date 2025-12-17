from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import auth, user, doctor, admin
from app.middleware.cors_middleware import setup_cors

app = FastAPI(title="Doctor Appointment System")
setup_cors(app)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(doctor.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.mount("/media", StaticFiles(directory="media"), name="media")
