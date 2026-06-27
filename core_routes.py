from fastapi import APProvider, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database_mysql import get_db
from app import models_mysql, supabase_client
from pydantic import BaseModel
from datetime import date

router = APIRouter()

# --- PYDANTIC SCHEMAS ---
class StudentCreate(BaseModel):
    name: str
    email: str
    class_id: int

class PaymentCreate(BaseModel):
    student_id: int
    amount: float
    date: str
    status: str

# --- ENDPOINTS ---

# 1. Kusajili Mwanafunzi (Local MySQL + Cloud Sync)
@router.post("/students/", tags=["Core School Management"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # A. Hifadhi kwenye local MySQL kwanza
    db_student = models_mysql.Student(name=student.name, email=student.email, class_id=student.class_id)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    # B. Trigger 1: Tuma automatic kwenda Supabase Cloud Auth
    supabase_client.sync_to_supabase_auth(student.email, student.name)
    
    return {"status": "Student created locally and synced to cloud auth", "data": {"id": db_student.id, "name": db_student.name}}

# 2. Kupata list ya wanafunzi (Kutoka Local MySQL pekee)
@router.get("/students/", tags=["Core School Management"])
def get_students(db: Session = Depends(get_db)):
    return db.query(models_mysql.Student).all()

# 3. Kurekodi Malipo (Bypasses MySQL, inenda moja kwa moja Supabase Cloud PostgreSQL)
@router.post("/payments/", tags=["Cloud Financial Management"])
def record_payment(payment: PaymentCreate):
    try:
        # Trigger 2: Inaruka MySQL na kuandika direct kwenye cloud database ya Supabase
        data, count = supabase_client.supabase.table("payment").insert({
            "student_id": payment.student_id,
            "amount": payment.amount,
            "date": payment.date,
            "status": payment.status
        }).execute()
        
        return {"status": "Financial record streamed directly to Supabase cloud", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloud write failed: {str(e)}")