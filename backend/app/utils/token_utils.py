def rough_token_count(text: str) -> int:
    # Very rough approximation for local checks.
    return max(1, len(text) // 4)
