from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models import TestSet
from app.schemas import TestSetCreate, TestSetResponse, TestSetUpdate

router = APIRouter()


@router.post("/testset/", response_model=TestSetResponse, status_code=201)
def create_test_set(test_set: TestSetCreate, db: Session = Depends(get_db)):
    db_test_set = TestSet(**test_set.model_dump())
    db.add(db_test_set)
    db.commit()
    db.refresh(db_test_set)
    return db_test_set


@router.get("/testset/", response_model=List[TestSetResponse])
def get_test_sets(offset: int = 0, limit: int = 33, db: Session = Depends(get_db)):
    return db.scalars(select(TestSet).offset(offset).limit(limit)).all()


@router.get("/testset/{test_set_id}", response_model=TestSetResponse)
def get_test_set(test_set_id: int, db: Session = Depends(get_db)):
    db_test_set = db.get(TestSet, test_set_id)
    if db_test_set is None:
        raise HTTPException(status_code=404, detail="Test set not found")
    return db_test_set


@router.put("/testset/{test_set_id}", response_model=TestSetResponse)
def update_test_set(test_set_id: int, test_set: TestSetUpdate, db: Session = Depends(get_db)):
    db_test_set = db.get(TestSet, test_set_id)
    if db_test_set is None:
        raise HTTPException(status_code=404, detail="Test set not found")
    for key, value in test_set.model_dump(exclude_unset=True).items():
        setattr(db_test_set, key, value)
    db.commit()
    db.refresh(db_test_set)
    return db_test_set


@router.delete("/testset/{test_set_id}", status_code=204)
def delete_test_set(test_set_id: int, db: Session = Depends(get_db)):
    db_test_set = db.get(TestSet, test_set_id)
    if db_test_set is None:
        raise HTTPException(status_code=404, detail="Test set not found")
    db.delete(db_test_set)
    db.commit()
    return None
