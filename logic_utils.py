ATTEMPT_LIMIT_MAP = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str): #REFACTORED: moved from app.py to logic_utils.py for better separation of concerns
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500  # Fixed: was 1-50, making Hard easier than Normal
    return 1, 100


def parse_guess(raw: str, low: int, high: int): #REFACACTORED from app.py # Fixed: added low/high params for range validation
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:  # Fixed: out-of-range guesses are now invalid
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret): #REFACACTORED from app.py
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📈 Go LOWER!"  # Fixed: was "Go HIGHER!" (wrong direction)
        else:
            return "Too Low", "📉 Go HIGHER!"  # Fixed: was "Go LOWER!" (wrong direction)
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go HIGHER!"
        return "Too Low", "📉 Go LOWER!"


def update_score(current_score: int, outcome: str, attempt_number: int): #REFACACTORED from app.py
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * attempt_number  # Fixed: was attempt_number + 1, overcounting attempts
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        return current_score - 5  # Fixed: was giving +5 bonus on even attempts for wrong guesses

    if outcome == "Too Low":
        return current_score - 5

    return current_score
