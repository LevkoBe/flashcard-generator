import google.generativeai as gai
from typing import List, Dict, Optional
import json
from app.config import settings


gai.configure(api_key=settings.gemini_api_key)

_model = gai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=(
        "You are a mnemonic flashcard generator. Create memorable flashcards "
        "using mnemonic techniques (visual imagery, word associations, acronyms, stories).\n"
        "Rules:\n"
        "- Each card's front and back must be ≤50 words\n"
        "- Front: A question or prompt\n"
        "- Back: A mnemonic answer (vivid, unusual, emotionally engaging)\n"
        "- Avoid dry definitions; make them memorable\n"
        "- Return valid JSON array only, no markdown formatting"
    )
)


async def generate_flashcards(
    text: str,
    guidance: Optional[str] = None,
    quantity: Optional[str] = None
) -> List[Dict[str, str]]:

    prompt = _build_prompt(text, guidance, quantity)
    response = _model.generate_content(prompt)
    return _parse_response(response.text)


def _build_prompt(
    text: str,
    guidance: Optional[str] = None,
    quantity: Optional[str] = None
) -> str:
    prompt = f"Generate flashcards from this text:\n\n{text}\n\n"

    if guidance:
        prompt += f"Focus on: {guidance}\n\n"
    if quantity:
        prompt += f"Generate exactly {quantity} flashcards.\n\n"
    else:
        prompt += "Generate 5-15 flashcards based on content richness.\n\n"

    prompt += (
        "Return JSON array:\n"
        "[\n"
        '  {"front": "question or term", "back": "mnemonic answer"}\n'
        "]"
    )
    return prompt


def _parse_response(response_text: str) -> List[Dict[str, str]]:

    json_text = response_text.strip()
    if json_text.startswith("```json"):
        json_text = json_text[7:]
    if json_text.startswith("```"):
        json_text = json_text[3:]
    if json_text.endswith("```"):
        json_text = json_text[:-3]
    json_text = json_text.strip()

    cards = json.loads(json_text)

    if not isinstance(cards, list):
        raise ValueError("AI-generated cards are not a list")
    for card in cards:
        if not isinstance(card, dict) or set(card.keys()) != {"front", "back"}:
            raise ValueError("AI-generated card is of incorrect format")

    return cards
