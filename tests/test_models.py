from app.models import TestSet, TestCard, Score


def test_models_import():
    assert TestSet is not None
    assert TestCard is not None
    assert Score is not None


def test_test_set_tablename():
    assert TestSet.__tablename__ == "test_sets"


def test_test_card_tablename():
    assert TestCard.__tablename__ == "test_cards"


def test_score_tablename():
    assert Score.__tablename__ == "scores"
