
from fastapi import APIRouter, HTTPException
from app.supabase_client import supabase
from pydantic import BaseModel
from datetime import date

router = APIRouter(prefix="/payments", tags=["Payments"])

class PaymentCreate(BaseModel):
    student_id: int
    amount: float
    status: str

@router.post("/")
def record_payment(payment: PaymentCreate):
    """
    Workflow Trigger 2: Bypasses the offline MySQL layer completely 
    and writes directly to the cloud Supabase PostgreSQL table.
    """
    try:
        data = {
            "student_id": payment.student_id,
            "amount": payment.amount,
            "date": str(date.today()),
            "status": payment.status
        }
        response = supabase.table("payment").insert(data).execute()
        return {"status": "Cloud Payment Logged", "data": response.data}
    except Exception as e:
        raise HTTPException(status_status=500, detail=f"Cloud write failed: {str(e)}")