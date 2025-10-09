import httpx
import trafilatura


async def extract_text(source_type: str, source_content: str) -> str:
    if source_type == "text":
        return source_content

    elif source_type == "url":
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(source_content)
            response.raise_for_status()

        extracted = trafilatura.extract(response.text)

        if extracted is None:
            raise ValueError("Could not extract text from URL")

        return extracted

    else:
        raise ValueError(f"Invalid source_type: {source_type}")
