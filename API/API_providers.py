from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

# שים לב: שיניתי את הייבוא בהתאם לקובץ יצירת ה-DB שלך
from create_db import Provider, RegularClient 
from database import get_db # מומלץ לשים את get_db בקובץ נפרד, תכף נראה את זה

router = APIRouter(
    prefix="/providers",
    tags=["Providers"]
)

# 5. הגדרת "סכימה" של Pydantic - זה מגדיר איזה מידע ה-API מצפה לקבל מהמשתמש
class ProviderCreateSchema(BaseModel):
    phone: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


# בקשת POST: יצירת בעל מקצוע חדש במערכת
@router.post("/providers/", response_model=ProviderCreateSchema)
def create_provider(provider_data: ProviderCreateSchema, db: Session = Depends(get_db)):
    # יצירת אובייקט חדש לפי המודל של SQLAlchemy
    new_provider = Provider(
        phone=provider_data.phone,
        first_name=provider_data.first_name,
        last_name=provider_data.last_name, 
        proffesion=provider_data.profession,
        is_avaliable=provider_data.is_available
    )
    # שמירה בבסיס הנתונים
    db.add(new_provider)
    db.commit()
    db.refresh(new_provider)
    return new_provider
# בקשת GET: שליפת כל בעלי המקצוע הקיימים במערכת
@router.get("/providers/")
def get_all_providers(db: Session = Depends(get_db)):
    providers = db.query(Provider).all()
    return providers

# הנתיב המעשי יהיה: PATCH /providers/{provider_id}
@router.patch("/{provider_id}")
def update_provider(provider_id: str, provider_data: ProviderCreateSchema, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    update_data = provider_data.model_dump(exclude_unset=True)  

    for key, value in update_data.items():
        setattr(provider, key, value)
    
    db.commit()
    db.refresh(provider)
    return provider

# הנתיב המעשי יהיה: DELETE /providers/{provider_id}
@router.delete("/{provider_id}")
def delete_provider(provider_id: str, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    db.delete(provider)
    db.commit()
    return {"detail": "Provider deleted successfully"}
#dfggsdf