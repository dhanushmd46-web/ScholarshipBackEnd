from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.user import UserTable
from models.scholarship import ScholarshipTable
from schemas.scholarship import UserScholarshipCreate, UserScholarshipResponse
from dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserScholarshipResponse])
def get_all_scholarships(
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    return db.query(ScholarshipTable).all()

@router.get("/{id}", response_model=UserScholarshipResponse)
def get_scholarship_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    scholarship = db.query(ScholarshipTable).filter(ScholarshipTable.id == id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship

@router.post("/", response_model=UserScholarshipResponse, status_code=201)
def create_scholarship(
    scholarship_data: UserScholarshipCreate,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can post scholarships")
    new_scholarship = ScholarshipTable(
        name=scholarship_data.name,
        description=scholarship_data.description,
        amount=scholarship_data.amount,
        deadline=scholarship_data.deadline,
        eligibility=scholarship_data.eligibility,
    )
    db.add(new_scholarship)
    db.commit()
    db.refresh(new_scholarship)
    return new_scholarship

@router.put("/{id}", response_model=UserScholarshipResponse)
def update_scholarship(
    id: int,
    scholarship_data: UserScholarshipCreate,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update scholarships")
    scholarship = db.query(ScholarshipTable).filter(ScholarshipTable.id == id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    scholarship.name = scholarship_data.name
    scholarship.description = scholarship_data.description
    scholarship.amount = scholarship_data.amount
    scholarship.deadline = scholarship_data.deadline
    scholarship.eligibility = scholarship_data.eligibility

    db.commit()
    db.refresh(scholarship)
    return scholarship

@router.delete("/{id}", status_code=200)
def delete_scholarship(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete scholarships")

    scholarship = db.query(ScholarshipTable).filter(ScholarshipTable.id == id).first()
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    deleted_info = {
        "id": scholarship.id,
        "name": scholarship.name,
        "description": scholarship.description,
        "amount": scholarship.amount,
    }
    db.delete(scholarship)
    db.commit()
    return {
        "message": f"Scholarship {id} deleted successfully",
        "deleted_record": deleted_info,
    }