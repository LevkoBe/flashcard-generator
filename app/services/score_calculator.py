from rapidfuzz import fuzz


def calculate_similarity(text1: str, text2: str):
    similarity = fuzz.token_sort_ratio(
        text1.lower().strip(),
        text2.lower().strip()
    )
    return similarity / 100.0


def is_correct(score: float, threshold: float = 0.7):
    return score >= threshold
