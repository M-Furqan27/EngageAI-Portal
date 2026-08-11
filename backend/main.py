# """
# backend/main.py

# REPLACE the existing file. Sirf representatives router add hua hai neeche.
# """

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI(title="EngageAI API", version="1.0.0")

# # Streamlit frontend se calls allow karne ke liye
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # dev ke liye; production mein specific origin daalna
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def health_check():
#     return {"status": "ok", "message": "EngageAI backend is running"}


# # ---------------- Module routers (add as each module is built) ----------------
# from modules.auth.router import router as auth_router
# app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# from modules.profile.router import router as profile_router
# app.include_router(profile_router, prefix="/profile", tags=["Profile"])

# from modules.admin.router import router as admin_router
# app.include_router(admin_router, prefix="/admin", tags=["Admin"])


# from modules.knowledge.router import router as knowledge_router
# app.include_router(knowledge_router, prefix="/knowledge", tags=["Knowledge"])


# from modules.leads.router import router as leads_router
# app.include_router(leads_router, prefix="/leads", tags=["Leads"])

# from modules.workflows.router import router as workflows_router
# app.include_router(workflows_router, prefix="/workflows", tags=["Workflows"])

# from modules.dashboard.router import router as dashboard_router
# app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])

# from modules.representatives.router import router as representatives_router
# app.include_router(representatives_router, prefix="/representatives", tags=["Representatives"])
# # ... (baaki modules isi tarah add honge jab wo ban jayen)


"""
backend/main.py
EngageAI Portal FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine

# Routers
from modules.auth.router import router as auth_router
from modules.profile.router import router as profile_router
from modules.admin.router import router as admin_router
from modules.dashboard.router import router as dashboard_router
from modules.knowledge.router import router as knowledge_router
from modules.leads.router import router as leads_router
from modules.representatives.router import router as representatives_router
from modules.workflows.router import router as workflows_router
from modules.auth.models import User
from modules.profile.organization_model import Organization
from modules.representatives.models import Representative, CalendarConnection

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="EngageAI Portal API",
    version="1.0.0",
    description="AI Customer Engagement Portal Backend"
)


# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=[
        "*"
    ],
    allow_headers=[
        "*"
    ],
)



# ---------------- ROUTERS ----------------


# Authentication
app.include_router(
    auth_router,
    tags=["Auth"]
)


# Profile
app.include_router(
    profile_router,
    prefix="/profile",
    tags=["Profile"]
)


# Admin
app.include_router(
    admin_router,
    prefix="/admin",
    tags=["Admin"]
)


# Dashboard
app.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"]
)


# Knowledge Base
app.include_router(
    knowledge_router,
    prefix="/knowledge",
    tags=["Knowledge"]
)


# Leads
app.include_router(
    leads_router,
    prefix="/leads",
    tags=["Leads"]
)


# Representatives
app.include_router(
    representatives_router,
    tags=["Representatives"]
)


# Workflows
app.include_router(
    workflows_router,
    prefix="/workflows",
    tags=["Workflows"]
)



# ---------------- HEALTH CHECK ----------------


@app.get("/")
def root():
    return {
        "status": "running",
        "message": "EngageAI Portal API is live"
    }