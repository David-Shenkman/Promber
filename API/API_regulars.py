from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

# ייבוא המודל והחיבור ל-DB
from create_db import RegularClient 
from database import get_db 

router = APIRouter(
    prefix="/regulars",
    tags=["Regular Clients"]
)

# סכמה ליצירה (שדות חובה)
class RegularCreateSchema(BaseModel):
    phone: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

# סכמה לעדכון (כל השדות אופציונליים)
class RegularUpdateSchema(BaseModel):
    phone: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# 1. בקשת POST: יצירת לקוח קבוע חדש
@router.post("/", response_model=RegularCreateSchema)
def create_regular(regular_data: RegularCreateSchema, db: Session = Depends(get_db)):
    new_regular = RegularClient(
        phone=regular_data.phone,
        first_name=regular_data.first_name,
        last_name=regular_data.last_name
    )
    db.add(new_regular)
    db.commit()
    db.refresh(new_regular)
    return new_regular

# 2. בקשת GET: שליפת כל הלקוחות הקבועים
@router.get("/")
def get_all_regulars(db: Session = Depends(get_db)):
    return db.query(RegularClient).all()

# 3. בקשת PATCH: עדכון שדה ספציפי (הגרסה המתוקנת והיחידה!)
@router.patch("/{regular_id}")
def update_regular(regular_id: str, regular_data: RegularUpdateSchema, db: Session = Depends(get_db)):
    regular = db.query(RegularClient).filter(RegularClient.id == regular_id).first()
    if not regular:
        raise HTTPException(status_code=404, detail="Regular client not found")
    
    # לוקח רק את השדות שהמשתמש שלח בפועל ב-JSON
    update_data = regular_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(regular, key, value)
        
    db.commit()
    db.refresh(regular)
    return regular

# 4. בקשת DELETE: מחיקת לקוח קבוע
@router.delete("/{regular_id}")
def delete_regular(regular_id: str, db: Session = Depends(get_db)):
    regular = db.query(RegularClient).filter(RegularClient.id == regular_id).first()
    if not regular:
        raise HTTPException(status_code=404, detail="Regular client not found")
    
    db.delete(regular)
    db.commit()
    return {"detail": "Regular deleted successfully"}
