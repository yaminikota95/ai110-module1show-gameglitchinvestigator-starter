from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    ATTEMPT_LIMIT_MAP,
)


# --- get_range_for_difficulty ---
# Bug fixed: Hard was returning (1, 50), making it easier than Normal

def test_hard_range_is_harder_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high, "Hard range should be larger than Normal"

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 500)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)


# --- parse_guess ---
# Bug fixed: guesses outside the difficulty range are now rejected

def test_parse_valid_guess():
    ok, value, err = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_too_high_rejected():
    ok, value, err = parse_guess("150", 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err

def test_parse_guess_too_low_rejected():
    ok, _, err = parse_guess("0", 1, 100)
    assert ok is False
    assert "between 1 and 100" in err

def test_parse_guess_empty():
    ok, _, err = parse_guess("", 1, 100)
    assert ok is False
    assert err == "Enter a guess."

def test_parse_guess_none():
    ok, _, err = parse_guess(None, 1, 100)
    assert ok is False
    assert err == "Enter a guess."

def test_parse_guess_non_numeric():
    ok, _, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert err == "That is not a number."

def test_parse_guess_decimal_truncated():
    ok, value, _ = parse_guess("7.9", 1, 100)
    assert ok is True
    assert value == 7

def test_parse_guess_boundary_low():
    ok, value, _ = parse_guess("1", 1, 100)
    assert ok is True
    assert value == 1

def test_parse_guess_boundary_high():
    ok, value, _ = parse_guess("100", 1, 100)
    assert ok is True
    assert value == 100


# --- check_guess ---
# Bug fixed: hint messages were swapped (Too High said "Go HIGHER", Too Low said "Go LOWER")

def test_correct_guess_returns_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_too_high_outcome():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_too_high_message_says_go_lower():
    # Bug fixed: was "Go HIGHER!" when guess was too high
    _, msg = check_guess(60, 50)
    assert "LOWER" in msg

def test_too_low_outcome():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

def test_too_low_message_says_go_higher():
    # Bug fixed: was "Go LOWER!" when guess was too low
    _, msg = check_guess(40, 50)
    assert "HIGHER" in msg


# --- update_score ---
# Bug fixed: score formula used attempt_number + 1 (overcounting)
# Bug fixed: "Too High" was giving +5 bonus on even attempts instead of always -5

def test_win_on_first_attempt_gives_90():
    # Bug fixed: was 100 - 10*(1+1) = 80, now 100 - 10*1 = 90
    score = update_score(0, "Win", 1)
    assert score == 90

def test_win_on_second_attempt_gives_80():
    score = update_score(0, "Win", 2)
    assert score == 80

def test_win_score_minimum_is_10():
    # attempt 10+: points floor at 10
    score = update_score(0, "Win", 15)
    assert score == 10

def test_too_high_always_deducts_5():
    # Bug fixed: was giving +5 on even attempts
    assert update_score(100, "Too High", 2) == 95
    assert update_score(100, "Too High", 3) == 95
    assert update_score(100, "Too High", 4) == 95

def test_too_low_deducts_5():
    assert update_score(100, "Too Low", 1) == 95

def test_unknown_outcome_unchanged():
    assert update_score(100, "SomethingElse", 1) == 100


# --- ATTEMPT_LIMIT_MAP ---

def test_attempt_limits():
    assert ATTEMPT_LIMIT_MAP["Easy"] == 6
    assert ATTEMPT_LIMIT_MAP["Normal"] == 8
    assert ATTEMPT_LIMIT_MAP["Hard"] == 5
