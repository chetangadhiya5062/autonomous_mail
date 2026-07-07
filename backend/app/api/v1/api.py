# backend/app/api/v1/api.py
from fastapi import APIRouter
# from app.api.v1.endpoints import emails, auth, agent
from app.api.v1.endpoints import (
    emails,
    auth,
    agent,
    benefits,
)

# Initialize the main v1 router
api_router = APIRouter()

# Include individual endpoint routers here
# Notice we define the specific prefix for emails here ("/emails")
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"]) 
api_router.include_router(emails.router, prefix="/emails", tags=["emails"])
api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
api_router.include_router(
    benefits.router,
    prefix="/benefits",
    tags=["Benefits RAG"],
)
# As we build more features, we just add them here:
# api_router.include_router(agent.router, prefix="/agent", tags=["agent"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])