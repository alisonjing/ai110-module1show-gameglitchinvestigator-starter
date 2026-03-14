from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# ── check_guess ────────────────────────────────────────────────────────────────

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# BUG FIX: hints were inverted — guess > secret said "Go HIGHER" instead of "Go LOWER"
def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint but got: {message}"

def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint but got: {message}"

# BUG FIX: secret was cast to str on even attempts, breaking int comparison
def test_check_guess_always_works_with_int_secret():
    # Should never raise TypeError or return wrong result regardless of attempt number
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# ── update_score ───────────────────────────────────────────────────────────────

# BUG FIX: off-by-one — formula was 100 - 10 * (attempt + 1), should be 100 - 10 * attempt
def test_win_on_first_attempt_gives_90_points():
    score = update_score(0, "Win", 1)
    assert score == 90, f"Expected 90 but got {score}"

def test_win_on_second_attempt_gives_80_points():
    score = update_score(0, "Win", 2)
    assert score == 80, f"Expected 80 but got {score}"

def test_win_score_never_goes_below_10():
    # At attempt 10+, points floor at 10
    score = update_score(0, "Win", 20)
    assert score == 10

def test_too_low_deducts_5():
    score = update_score(50, "Too Low", 1)
    assert score == 45

def test_too_high_even_attempt_adds_5():
    score = update_score(50, "Too High", 2)
    assert score == 55

def test_too_high_odd_attempt_deducts_5():
    score = update_score(50, "Too High", 1)
    assert score == 45


# ── parse_guess ────────────────────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_float_string_truncates_to_int():
    ok, value, err = parse_guess("3.7")
    assert ok is True
    assert value == 3

def test_parse_empty_string_returns_error():
    ok, value, _ = parse_guess("")
    assert ok is False
    assert value is None

def test_parse_none_returns_error():
    ok, _, _ = parse_guess(None)
    assert ok is False

def test_parse_non_numeric_returns_error():
    ok, _, err = parse_guess("abc")
    assert ok is False
    assert err == "That is not a number."


# ── get_range_for_difficulty ───────────────────────────────────────────────────

# BUG FIX: Normal and Hard ranges were swapped
def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) == (1, 20)

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert (low, high) == (1, 50)

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 100)

def test_hard_range_is_larger_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, "Hard should have a bigger range than Normal"
