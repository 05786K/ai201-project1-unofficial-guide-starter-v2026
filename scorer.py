import re


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s$.-]", "", text)
    return text.strip()


def judge(question, expects, answer, results) -> bool:
    """
    Return True if the expected answer appears in the generated answer.
    """
    if not answer or not expects:
        return False

    normalized_answer = normalize(answer)
    normalized_expects = normalize(expects)

    return normalized_expects in normalized_answer