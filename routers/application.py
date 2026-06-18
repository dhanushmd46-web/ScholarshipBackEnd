from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.user import UserTable
from models.application import ApplicationTable
from schemas.application import UserApplicationCreate, UserApplicationResponse
from dependencies import get_current_user

router = APIRouter()

@router.get("", response_model=List[UserApplicationResponse])
def get_all_application(
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role == "admin":
        return db.query(ApplicationTable).all()
    return db.query(ApplicationTable).filter(ApplicationTable.user_id == current_user.id).all()

@router.get("/{id}", response_model=UserApplicationResponse)
def get_Application_by_Id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    application_data = db.query(ApplicationTable).filter(ApplicationTable.id == id).first()
    if not application_data:
        raise HTTPException(status_code=404, detail="Application Not Found")
    if current_user.role != "admin" and application_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    return application_data

@router.post("", response_model=UserApplicationResponse)
def Create_Application(
    Application_data: UserApplicationCreate,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role == "admin":
        raise HTTPException(status_code=403, detail="Only User Can Create The Application")
    new_Application = ApplicationTable(
        scholarship_id=Application_data.scholarship_id,
        user_id=current_user.id,
        statement=Application_data.statement,
        applied_at=datetime.utcnow(),
        status='Under Review'
    )
    db.add(new_Application)
    db.commit()
    db.refresh(new_Application)
    return new_Application

@router.put("/{id}", response_model=UserApplicationResponse)
def update_scholarship(
    id: int,
    Application_data: UserApplicationResponse,
    db: Session = Depends(get_db),
    current_user: UserTable = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only Admin Can Update The Application")
    application_data = db.query(ApplicationTable).filter(ApplicationTable.id == id).first()
    if not application_data:
        raise HTTPException(status_code=404, detail="Application Not Found")
    application_data.scholarship_id = Application_data.scholarship_id
    application_data.user_id = Application_data.user_id
    application_data.statement = Application_data.statement
    application_data.applied_at = Application_data.applied_at
    application_data.status = Application_data.status

    db.commit()
    db.refresh(application_data)
    return application_data