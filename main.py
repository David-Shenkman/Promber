from fastapi import FastAPI
from API.API_regulars import router as regulars_router
from API.API_guests import router as guests_router
from API.API_providers import router as providers_router

# 🔥 השורה החייבת להופיע בדיוק בשם הזה:
app = FastAPI(title="FORCED API System")

# חיבור הראוטר
app.include_router(regulars_router)
app.include_router(guests_router)
app.include_router(providers_router)
@app.get("/")
def root():
    return {"message": "The FORCED API is running successfully!"}
