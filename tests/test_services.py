import pytest
from unittest.mock import patch, AsyncMock
from app.services.text_extractor import extract_text


@pytest.mark.asyncio
async def test_extract_text_from_raw_text():
    result = await extract_text("text", "Hello world")
    assert result == "Hello world"


@pytest.mark.asyncio
async def test_extract_text_from_url_success():
    mock_response = AsyncMock()
    mock_response.text = "<html><body><article>Extracted content</article></body></html>"
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with patch("trafilatura.extract", return_value="Extracted content"):
            result = await extract_text("url", "https://example.com")
            assert result == "Extracted content"


@pytest.mark.asyncio
async def test_extract_text_from_url_extraction_fails():
    mock_response = AsyncMock()
    mock_response.text = "<html><body>No article content</body></html>"
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        with patch("trafilatura.extract", return_value=None):
            with pytest.raises(ValueError, match="Could not extract text"):
                await extract_text("url", "https://example.com")


@pytest.mark.asyncio
async def test_extract_text_invalid_source_type():
    with pytest.raises(ValueError, match="Invalid source_type"):
        await extract_text("invalid", "content")


@pytest.mark.asyncio
async def test_extract_text_empty_text():
    result = await extract_text("text", "")
    assert result == ""
