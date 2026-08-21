from src.mission_schedule import (
    find_next_upcoming_pass
)


# ============================================================
# TEST TIME
# ============================================================
class TestTime:

    def __init__(
        self,
        value
    ):

        self.value = value
        self.tt = value

    def utc_strftime(
        self,
        format_string
    ):

        return self.value
# ============================================================
# ============================================================

class TestPass:

    def __init__(
        self,
        satellite_name,
        aos_time
    ):

        self.satellite_name = (
            satellite_name
        )

        self.aos_time = (
            aos_time
        )


# ============================================================
# CREATE TEST PASSES
# ============================================================

pass_1 = TestPass(
    "ISS (ZARYA)",
    TestTime(
        "2026-08-20 10:00:00"
    )
)

pass_2 = TestPass(
    "NOAA 19",
    TestTime(
        "2026-08-20 12:30:00"
    )
)

pass_3 = TestPass(
    "ISS (ZARYA)",
    TestTime(
        "2026-08-20 15:15:00"
    )
)

pass_4 = TestPass(
    "NOAA 19",
    TestTime(
        "2026-08-20 18:40:00"
    )
)


# ============================================================
# COMBINED SCHEDULE
# ============================================================

combined_schedule = [

    pass_1,
    pass_2,
    pass_3,
    pass_4
]


# ============================================================
# CURRENT TIME
# ============================================================

current_time = TestTime(
    "2026-08-20 13:00:00"
)


# ============================================================
# FIND NEXT PASS
# ============================================================

next_pass = (
    find_next_upcoming_pass(
        combined_schedule,
        current_time
    )
)


# ============================================================
# TEST RESULT
# ============================================================

assert (
    next_pass
    is pass_3
)


assert (
    next_pass.satellite_name
    == "ISS (ZARYA)"
)


# ============================================================
# TEST NO FUTURE PASS
# ============================================================

late_time = TestTime(
    "2026-08-20 20:00:00"
)

no_pass = (
    find_next_upcoming_pass(
        combined_schedule,
        late_time
    )
)


assert (
    no_pass
    is None
)


# ============================================================
# TEST EMPTY SCHEDULE
# ============================================================

empty_result = (
    find_next_upcoming_pass(
        [],
        current_time
    )
)


assert (
    empty_result
    is None
)


print(
    "\nNext upcoming pass "
    "tests passed."
)