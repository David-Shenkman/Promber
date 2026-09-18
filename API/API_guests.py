from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

# 🔥 תיקון 1: מייבאים את GuestClient (ולא את RegularClient)
from create_db import GuestClient 
from database import get_db 

# הגדרת הראוטר עם הקידומת המרכזית
router = APIRouter(
    prefix="/guests",
    tags=["Guests Clients"]
)

# סכימה ליצירה ועדכון
class GuestSchema(BaseModel):
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    class Config:
        from_attributes = True


# ========================================================
# 🔥 נקודות הקצה של ה-API (Endpoints) 🔥
# ========================================================

# 🔥 תיקון 2: משאירים רק "/" כי הקידומת "/guests" כבר מוגדרת למעלה בראוטר!
# הנתיב המעשי יהיה: POST /guests/
@router.post("/", response_model=GuestSchema)
def create_guest(guest_data: GuestSchema, db: Session = Depends(get_db)):
    new_guest = GuestClient(
        phone=guest_data.phone,
        first_name=guest_data.first_name,
        last_name=guest_data.last_name
    )
    db.add(new_guest)
    db.commit()
    db.refresh(new_guest)
    return new_guest

# הנתיב המעשי יהיה: GET /guests/
@router.get("/")
def get_all_guests(db: Session = Depends(get_db)):
    return db.query(GuestClient).all()
