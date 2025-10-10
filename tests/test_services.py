import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from app.services.text_extractor import extract_text
from app.services.score_calculator import calculate_similarity, is_correct
from app.services.flashcard_generator import (
    generate_flashcards,
    _build_prompt,
    _parse_response
)
import json


class TestTextExtractor:

    @pytest.mark.asyncio
    async def test_extract_text_from_raw_text(self):
        result = await extract_text("text", "Hello world")
        assert result == "Hello world"

    @pytest.mark.asyncio
    async def test_extract_text_from_url_success(self):
        mock_response = AsyncMock()
        mock_response.text = "<html><body><article>Extracted content</article></body></html>"
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            with patch("trafilatura.extract", return_value="Extracted content"):
                result = await extract_text("url", "https://example.com")
                assert result == "Extracted content"

    @pytest.mark.asyncio
    async def test_extract_text_from_url_extraction_fails(self):
        mock_response = AsyncMock()
        mock_response.text = "<html><body>No article content</body></html>"
        mock_response.raise_for_status = MagicMock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            with patch("trafilatura.extract", return_value=None):
                with pytest.raises(ValueError, match="Could not extract text"):
                    await extract_text("url", "https://example.com")

    @pytest.mark.asyncio
    async def test_extract_text_invalid_source_type(self):
        with pytest.raises(ValueError, match="Invalid source_type"):
            await extract_text("invalid", "content")

    @pytest.mark.asyncio
    async def test_extract_text_empty_text(self):
        result = await extract_text("text", "")
        assert result == ""


class TestScoreCalculator:

    def test_calculate_score_for_identical(self):
        score_value = calculate_similarity("Exactly the same", "Exactly the same")
        assert score_value == 1.0

    def test_calculate_score_for_very_similar(self):
        score_value = calculate_similarity("Exactly the same", "The same. Exactly!")
        assert score_value > 0.9

    def test_calculate_score_for_similar(self):
        score_value = calculate_similarity("Exactly the same", "Exactly, The Sam")
        assert score_value > 0.5
        assert score_value < 1.0

    def test_calculate_score_for_different(self):
        score_value = calculate_similarity("Exactly the same", "Very much not so")
        assert score_value < 0.5

    def test_is_correct(self):
        correct = is_correct(score=0.8, threshold=0.7)
        assert correct

    def test_is_not_correct(self):
        correct = is_correct(score=0.6, threshold=0.7)
        assert not correct


class TestFlashcardGenerator:

    def test_build_prompt_minimal(self):
        prompt = _build_prompt("Sample text", None, None)
        assert "Sample text" in prompt
        assert "5-15 flashcards" in prompt
        assert "JSON array" in prompt

    def test_build_prompt_with_guidance(self):
        prompt = _build_prompt("Sample text", "focus on verbs", None)
        assert "Focus on: focus on verbs" in prompt

    def test_build_prompt_with_quantity(self):
        prompt = _build_prompt("Sample text", None, 10)
        assert "exactly 10 flashcards" in prompt

    def test_build_prompt_with_both_params(self):
        prompt = _build_prompt("Sample text", "definitions only", 5)
        assert "Focus on: definitions only" in prompt
        assert "exactly 5 flashcards" in prompt

    def test_parse_response_valid_json(self):
        response = '[{"front": "Q1", "back": "A1"}, {"front": "Q2", "back": "A2"}]'
        cards = _parse_response(response)
        assert len(cards) == 2
        assert cards[0]["front"] == "Q1"
        assert cards[1]["back"] == "A2"

    def test_parse_response_with_markdown_wrapper(self):
        response = '```json\n[{"front": "Q1", "back": "A1"}]\n```'
        cards = _parse_response(response)
        assert len(cards) == 1
        assert cards[0]["front"] == "Q1"

    def test_parse_response_with_backticks_only(self):
        response = '```\n[{"front": "Q1", "back": "A1"}]\n```'
        cards = _parse_response(response)
        assert len(cards) == 1

    def test_parse_response_invalid_json(self):
        with pytest.raises(json.JSONDecodeError):
            _parse_response("not valid json")

    def test_parse_response_not_a_list(self):
        with pytest.raises(ValueError, match="not a list"):
            _parse_response('{"front": "Q1", "back": "A1"}')

    def test_parse_response_missing_front(self):
        with pytest.raises(ValueError, match="incorrect format"):
            _parse_response('[{"back": "A1"}]')

    def test_parse_response_missing_back(self):
        with pytest.raises(ValueError, match="incorrect format"):
            _parse_response('[{"front": "Q1"}]')

    def test_parse_response_empty_array(self):
        cards = _parse_response('[]')
        assert cards == []

    @pytest.mark.asyncio
    async def test_generate_flashcards_success(self):
        mock_response = MagicMock()
        mock_response.text = '[{"front": "Question?", "back": "Answer."}]'

        with patch(
            "app.services.flashcard_generator._model.generate_content",
            return_value=mock_response
        ):
            cards = await generate_flashcards("Sample text about X")
            assert len(cards) == 1
            assert cards[0]["front"] == "Question?"

    @pytest.mark.asyncio
    async def test_generate_flashcards_with_params(self):
        mock_response = MagicMock()
        mock_response.text = '[{"front": "Q", "back": "A"}]'

        with patch(
            "app.services.flashcard_generator._model.generate_content",
            return_value=mock_response
        ) as mock_gen:
            cards = await generate_flashcards("Text", guidance="verbs", quantity=5)
            assert len(cards) == 1

            call_args = mock_gen.call_args[0][0]
            assert "Focus on: verbs" in call_args
            assert "exactly 5" in call_args
