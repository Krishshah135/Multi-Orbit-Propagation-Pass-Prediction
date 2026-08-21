from src.mission_schedule import (
    rank_passes_by_elevation
)


# ============================================================
# TEST PASS
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

pass_1 = TestPass(
    "ISS (ZARYA)",
    35.0,
    5.0
)

pass_2 = TestPass(
    "NOAA 19",
    72.0,
    8.0
)

pass_3 = TestPass(
    "ISS (ZARYA)",
    51.0,
    6.0
)

pass_4 = TestPass(
    "NOAA 19",
    28.0,
    4.0
)


combined_schedule = [
    pass_1,
    pass_2,
    pass_3,
    pass_4
]


# ============================================================
# RANK PASSES
# ============================================================

ranked_passes = (
    rank_passes_by_elevation(
        combined_schedule
    )
)


# ============================================================
# TEST COUNT
# ============================================================

assert (
    len(ranked_passes)
    == 4
)


# ============================================================
# TEST ORDER
# ============================================================

assert (
    ranked_passes[0]
    is pass_2
)

assert (
    ranked_passes[1]
    is pass_3
)

assert (
    ranked_passes[2]
    is pass_1
)

assert (
    ranked_passes[3]
    is pass_4
)


# ============================================================
# TEST EMPTY SCHEDULE
# ============================================================

assert (
    rank_passes_by_elevation([])
    == []
)


print(
    "\nPass ranking "
    "tests passed."
)