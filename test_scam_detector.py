from scam_detector import analyze_message, HIGH, POSSIBLE, SAFE


def test_obvious_scam_is_high_risk():
    result = analyze_message(
        "URGENT! You won a free iPhone! Click here now!"
    )

    assert result.level == "high"
    assert result.score >= 3


def test_normal_message_is_safe():
    result = analyze_message(
        "Hey, are you coming to school today?"
    )

    assert result.level == "safe"


def test_word_inside_another_word_is_not_flagged():
    result = analyze_message(
        "Freezing outside, bring a jacket"
    )

    assert result.score == 0


def test_plain_link_is_not_high_risk():
    result = analyze_message(
        "Class photos are here: www.school.ca"
    )

    assert result.level != "high"


def test_shortened_link_with_pressure_is_high_risk():
    result = analyze_message(
        "Urgent! Verify here: http://bit.ly/abc123"
    )

    assert result.level == "high"

def test_gift_card_payment_demand_is_high_risk():
    result = analyze_message("You owe $500. Pay immediately using an Apple gift card.")
    assert result.level == "high"

def test_account_deletion_threat_is_high_risk():
    result = analyze_message("Your Instagram account will be deleted in 24 hours unless you log in here")
    assert result.level == "high"
