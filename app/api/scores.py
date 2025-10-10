from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models import TestCard, Score
from app.schemas import ScoreCreate, ScoreResult
from app.services.score_calculator import calculate_similarity, is_correct


router = APIRouter()


@router.post(
    "/testset/{test_set_id}/testcard/{test_card_id}/score",
    response_model=ScoreResult,
    status_code=201
)
def create_score(
    test_set_id: int,
    test_card_id: int,
    score_create: ScoreCreate,
    db: Session = Depends(get_db)
):
    card = db.execute(
        select(TestCard).where(TestCard.id == test_card_id, TestCard.test_set_id == test_set_id)
    ).scalar_one_or_none()

    if not card:
        return HTTPException(status_code=500, detail="No card with the specified ID found.")

    score_value = calculate_similarity(card.back_side, score_create.user_answer)
    correct = is_correct(score_value)

    db_score = Score(
        card_id=test_card_id,
        score=score_value,
        user_answer=score_create.user_answer
    )
    db.add(db_score)
    db.commit()

    return ScoreResult(
        score=score_value,
        correct=correct,
        expected=card.back_side
    )
