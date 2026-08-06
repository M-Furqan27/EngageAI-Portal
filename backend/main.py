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


from fastapi import FastAPI

from core.database import (
    Base,
    engine,
)


# Import existing Portal routers
from modules.auth.router import (
    router as auth_router
)

from modules.knowledge.router import (
    router as knowledge_router
)

from modules.leads.router import (
    router as leads_router
)

from modules.dashboard.router import (
    router as dashboard_router
)


# NEW REAL REPRESENTATIVE MODULE

from modules.representatives.router import (
    router as representatives_router
)



# Create database tables

Base.metadata.create_all(
    bind=engine
)



app = FastAPI(
    title="EngageAI Portal API",
    version="1.0.0",
)





# Existing modules

app.include_router(
    auth_router
)


app.include_router(
    knowledge_router
)


app.include_router(
    leads_router
)


app.include_router(
    dashboard_router
)




# Representative module

app.include_router(
    representatives_router
)





@app.get("/")
def root():

    return {

        "message":
            "EngageAI Portal API running"

    }