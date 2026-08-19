import csv
import os

from src.mission_schedule import (
    export_combined_schedule
)


class TestTime:

    def utc_strftime(
        self,
        format_string
    ):
        return "2026-08-19 00:00:00 UTC"


class TestPass:

    satellite_name = "ISS (ZARYA)"
    aos_time = TestTime()
    max_elevation_deg = 65.0
    max_elevation_time = TestTime()
    los_time = TestTime()
    duration_minutes = 8.0
    elevation_mask_deg = 10.0


filename = (
    "output/test_combined_schedule.csv"
)


export_combined_schedule(
    [TestPass()],
    filename,
    "Chennai",
    13.0827,
    80.2707,
    TestTime(),
    720,
    10,
    10.0
)


assert os.path.exists(
    filename
)


with open(
    filename,
    "r",
    encoding="utf-8"
) as file:

    rows = list(
        csv.reader(file)
    )


# Verify satellite appears
assert any(
    "ISS (ZARYA)" in row
    for row in rows
)


# Verify duration appears
assert any(
    "8.00" in row
    for row in rows
)


print(
    "\nCombined schedule export test passed."
)