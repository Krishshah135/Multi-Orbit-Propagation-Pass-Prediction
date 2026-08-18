from src.prediction_config import (
    create_prediction_config,
    print_prediction_config
)


# ============================================================
# CREATE CONFIGURATION
# ============================================================

config = create_prediction_config(
    duration_minutes=720,
    step_seconds=10,
    elevation_mask_deg=10.0
)


# ============================================================
# DISPLAY CONFIGURATION
# ============================================================

print_prediction_config(
    config
)


# ============================================================
# TEST VALUES
# ============================================================

assert (
    config["duration_minutes"]
    == 720
)

assert (
    config["step_seconds"]
    == 10
)

assert (
    config["elevation_mask_deg"]
    == 10.0
)


# ============================================================
# TEST INVALID VALUES
# ============================================================

try:

    create_prediction_config(
        duration_minutes=-1
    )

    raise AssertionError(
        "Negative duration was accepted."
    )

except ValueError:

    pass


try:

    create_prediction_config(
        step_seconds=0
    )

    raise AssertionError(
        "Zero step was accepted."
    )

except ValueError:

    pass


try:

    create_prediction_config(
        elevation_mask_deg=100
    )

    raise AssertionError(
        "Invalid elevation mask was accepted."
    )

except ValueError:

    pass


print(
    "\nPrediction configuration "
    "tests passed."
)