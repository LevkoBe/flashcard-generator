from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models import TestSet, TestCard
from app.schemas import TestCardCreate, TestCardUpdate, TestCardResponse

router = APIRouter()


@router.post(
    "/testset/{test_set_id}/testcard/",
    response_model=TestCardResponse,
    status_code=201
)
def create_test_card(
    test_set_id: int,
    test_card: TestCardCreate,
    db: Session = Depends(get_db)
):
    test_set = db.execute(
        select(TestSet).where(TestSet.id == test_set_id)
    ).scalar_one_or_none()
    if not test_set:
        raise HTTPException(status_code=404, detail="TestSet not found")

    db_test_card = TestCard(**test_card.model_dump(), test_set_id=test_set_id)
    db.add(db_test_card)
    db.commit()
    db.refresh(db_test_card)
    return db_test_card


@router.get(
    "/testset/{test_set_id}/testcard/",
    response_model=List[TestCardResponse]
)
def get_test_cards(test_set_id: int, db: Session = Depends(get_db)):
    test_set = db.execute(
        select(TestSet).where(TestSet.id == test_set_id)
    ).scalar_one_or_none()
    if not test_set:
        raise HTTPException(status_code=404, detail="TestSet not found")

    cards = db.execute(
        select(TestCard)
        .where(TestCard.test_set_id == test_set_id)
        .order_by(TestCard.position)
    ).scalars().all()
    return cards


@router.get(
    "/testset/{test_set_id}/testcard/{card_id}",
    response_model=TestCardResponse
)
def get_test_card(test_set_id: int, card_id: int, db: Session = Depends(get_db)):
    card = db.execute(
        select(TestCard)
        .where(TestCard.id == card_id, TestCard.test_set_id == test_set_id)
    ).scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="TestCard not found")
    return card


@router.put(
    "/testset/{test_set_id}/testcard/{card_id}",
    response_model=TestCardResponse
)
def update_test_card(
    test_set_id: int,
    card_id: int,
    card_update: TestCardUpdate,
    db: Session = Depends(get_db)
):
    card = db.execute(
        select(TestCard)
        .where(TestCard.id == card_id, TestCard.test_set_id == test_set_id)
    ).scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="TestCard not found")

    update_data = card_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(card, key, value)

    db.commit()
    db.refresh(card)
    return card


@router.delete(
    "/testset/{test_set_id}/testcard/{card_id}",
    status_code=204
)
def delete_test_card(test_set_id: int, card_id: int, db: Session = Depends(get_db)):
    card = db.execute(
        select(TestCard)
        .where(TestCard.id == card_id, TestCard.test_set_id == test_set_id)
    ).scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="TestCard not found")

    db.delete(card)
    db.commit()
    return None
