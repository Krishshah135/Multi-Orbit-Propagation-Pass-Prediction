from src.mission_schedule import (
    calculate_schedule_statistics
)


# ============================================================
# TEST PASS OBJECT
# ============================================================

class TestPass:

    def __init__(
        self,
        satellite_name,
        max_elevation_deg,
        duration_minutes
    ):

        self.satellite_name = (
            satellite_name
        )

        self.max_elevation_deg = (
            max_elevation_deg
        )

        self.duration_minutes = (
            duration_minutes
        )


# ============================================================
# TEST DATA
# ============================================================

test_schedule = [

    TestPass(
        "ISS (ZARYA)",
        65.0,
        8.0
    ),

    TestPass(
        "NOAA 19",
        30.0,
        5.0
    ),

    TestPass(
        "ISS (ZARYA)",
        42.0,
        6.0
    ),

    TestPass(
        "NOAA 19",
        55.0,
        7.0
    )
]


# ============================================================
# CALCULATE STATISTICS
# ============================================================

statistics = (
    calculate_schedule_statistics(
        test_schedule
    )
)


# ============================================================
# TEST TOTAL PASSES
# ============================================================

assert (
    statistics["total_passes"]
    == 4
)


# ============================================================
# TEST SATELLITE COUNT
# ============================================================

assert (
    statistics["total_satellites"]
    == 2
)


# ============================================================
# TEST AVERAGE DURATION
# ============================================================

expected_average = (
    (8.0 + 5.0 + 6.0 + 7.0)
    / 4
)

assert (
    abs(
        statistics[
            "average_duration_minutes"
        ]
        - expected_average
    )
    < 1e-9
)


# ============================================================
# TEST HIGHEST ELEVATION
# ============================================================

assert (
    statistics[
        "highest_elevation_deg"
    ]
    == 65.0
)


# ============================================================
# TEST LONGEST PASS
# ============================================================

assert (
    statistics[
        "longest_duration_minutes"
    ]
    == 8.0
)


# ============================================================
# TEST EMPTY SCHEDULE
# ============================================================

empty_statistics = (
    calculate_schedule_statistics(
        []
    )
)

assert (
    empty_statistics[
        "total_passes"
    ]
    == 0
)

assert (
    empty_statistics[
        "total_satellites"
    ]
    == 0
)

assert (
    empty_statistics[
        "highest_elevation_deg"
    ]
    is None
)


print(
    "\nSchedule statistics "
    "tests passed."
)