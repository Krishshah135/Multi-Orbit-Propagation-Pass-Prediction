from src.prediction_report import (
    build_prediction_report,
    print_prediction_report
)


# ============================================================
# TEST DATA
# ============================================================

test_passes = [

    {
        "max_elevation_deg": 25.0,
        "duration_seconds": 300,
        "aos_time": "2026-08-18 10:00:00 UTC",
        "max_elevation_time": "2026-08-18 10:02:30 UTC",
        "los_time": "2026-08-18 10:05:00 UTC"
    },

    {
        "max_elevation_deg": 65.0,
        "duration_seconds": 480,
        "aos_time": "2026-08-18 11:00:00 UTC",
        "max_elevation_time": "2026-08-18 11:04:00 UTC",
        "los_time": "2026-08-18 11:08:00 UTC"
    },

    {
        "max_elevation_deg": 40.0,
        "duration_seconds": 240,
        "aos_time": "2026-08-18 12:00:00 UTC",
        "max_elevation_time": "2026-08-18 12:02:00 UTC",
        "los_time": "2026-08-18 12:04:00 UTC"
    }
]


# ============================================================
# BUILD REPORT
# ============================================================

report = build_prediction_report(
    test_passes
)


# ============================================================
# DISPLAY REPORT
# ============================================================

print_prediction_report(
    report
)


# ============================================================
# TEST TOTAL PASSES
# ============================================================

assert (
    report["total_passes"]
    == 3
)


# ============================================================
# TEST BEST PASS
# ============================================================

assert (
    report["best_pass"]
    ["max_elevation_deg"]
    == 65.0
)


# ============================================================
# TEST LONGEST PASS
# ============================================================

assert (
    report["longest_pass"]
    ["duration_seconds"]
    == 480
)


# ============================================================
# TEST AVERAGE DURATION
# ============================================================

expected_average = (
    (300 + 480 + 240)
    / 3
    / 60
)

assert (
    abs(
        report[
            "average_duration_minutes"
        ]
        - expected_average
    )
    < 1e-9
)


# ============================================================
# TEST NO-PASS CONDITION
# ============================================================

empty_report = (
    build_prediction_report([])
)


assert (
    empty_report["total_passes"]
    == 0
)

assert (
    empty_report["best_pass"]
    is None
)


print(
    "\nPrediction report tests passed."
)