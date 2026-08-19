from src.mission_schedule import (
    build_combined_schedule,
    print_combined_schedule
)


# ============================================================
# SIMPLE TEST PASS OBJECT
# ============================================================


class TestPass:

    def __init__(
        self,
        satellite_name,
        aos_time,
        max_elevation_deg,
        duration_minutes
    ):

        self.satellite_name = (
            satellite_name
        )

        self.aos_time = aos_time

        self.max_elevation_deg = (
            max_elevation_deg
        )

        self.duration_minutes = (
            duration_minutes
        )


# ============================================================
# TEST TIME OBJECT
# ============================================================


class TestTime:

    def __init__(
        self,
        value
    ):

        self.value = value

    def __lt__(
        self,
        other
    ):

        return (
            self.value
            < other.value
        )

    def utc_strftime(
        self,
        format_string
    ):

        return self.value


# ============================================================
# TEST DATA
# ============================================================


iss_pass_1 = TestPass(
    "ISS (ZARYA)",
    TestTime(
        "2026-08-19 03:00:00"
    ),
    65.0,
    8.0
)


iss_pass_2 = TestPass(
    "ISS (ZARYA)",
    TestTime(
        "2026-08-19 07:00:00"
    ),
    42.0,
    6.0
)


noaa_pass_1 = TestPass(
    "NOAA 19",
    TestTime(
        "2026-08-19 01:00:00"
    ),
    30.0,
    5.0
)


noaa_pass_2 = TestPass(
    "NOAA 19",
    TestTime(
        "2026-08-19 05:00:00"
    ),
    55.0,
    7.0
)


# ============================================================
# BUILD TEST CATALOG
# ============================================================


all_predictions = {

    "ISS (ZARYA)": {

        "pass_results": [
            iss_pass_1,
            iss_pass_2
        ]
    },

    "NOAA 19": {

        "pass_results": [
            noaa_pass_1,
            noaa_pass_2
        ]
    }
}


# ============================================================
# BUILD COMBINED SCHEDULE
# ============================================================


combined_schedule = (
    build_combined_schedule(
        all_predictions
    )
)


# ============================================================
# TEST NUMBER OF PASSES
# ============================================================


assert (
    len(combined_schedule)
    == 4
)


# ============================================================
# TEST CHRONOLOGICAL ORDER
# ============================================================


assert (
    combined_schedule[0]
    is noaa_pass_1
)


assert (
    combined_schedule[1]
    is iss_pass_1
)


assert (
    combined_schedule[2]
    is noaa_pass_2
)


assert (
    combined_schedule[3]
    is iss_pass_2
)


# ============================================================
# PRINT TEST RESULT
# ============================================================


print_combined_schedule(
    combined_schedule
)


print(
    "\nMission schedule "
    "tests passed."
)