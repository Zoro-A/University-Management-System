from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_route import router as auth_router
from routes.student_route import router as student_router
from routes.admin_route import router as admin_router
from routes.faculty_route import router as faculty_router

app = FastAPI(title="University Management System API")

# ----- CORS (Vue Frontend Allowed) -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow Vue frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Register Routers -----
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(admin_router)
app.include_router(faculty_router)

@app.get("/")
def root():
    return {"message": "University Management System Backend Running"}
