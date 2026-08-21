# ============================================================
# COMBINED MISSION SCHEDULE
# ============================================================


def build_combined_schedule(
    all_predictions
):
    """
    Combine pass results from all satellites
    into one chronological mission schedule.
    """

    combined_schedule = []

    # --------------------------------------------------------
    # Collect passes from every satellite
    # --------------------------------------------------------

    for satellite_name, prediction in (
        all_predictions.items()
    ):

        pass_results = prediction[
            "pass_results"
        ]

        for pass_result in pass_results:

            combined_schedule.append(
                pass_result
            )

    # --------------------------------------------------------
    # Sort by AOS
    # --------------------------------------------------------

    combined_schedule.sort(
        key=lambda pass_result:
            pass_result.aos_time
    )

    return combined_schedule


# ============================================================
# PRINT COMBINED SCHEDULE
# ============================================================


def print_combined_schedule(
    combined_schedule
):
    """
    Print the combined chronological
    mission schedule.
    """

    print(
        "\n" + "=" * 90
    )

    print(
        "                    COMBINED MISSION SCHEDULE"
    )

    print(
        "=" * 90
    )

    # --------------------------------------------------------
    # No passes
    # --------------------------------------------------------

    if not combined_schedule:

        print(
            "\nNo visible satellite passes "
            "were detected."
        )

        print(
            "=" * 90
        )

        return

    # --------------------------------------------------------
    # Table header
    # --------------------------------------------------------

    print(
        f"{'AOS':<24}"
        f"{'SATELLITE':<20}"
        f"{'MAX EL.':>12}"
        f"{'DURATION':>14}"
    )

    print(
        "-" * 90
    )

    # --------------------------------------------------------
    # Print passes
    # --------------------------------------------------------

    for pass_result in combined_schedule:

        aos_string = (
            pass_result.aos_time
            .utc_strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        print(
            f"{aos_string:<24}"
            f"{pass_result.satellite_name:<20}"
            f"{pass_result.max_elevation_deg:>10.2f}°"
            f"{pass_result.duration_minutes:>11.2f} min"
        )

    print(
        "-" * 90
    )

    print(
        f"Total passes: "
        f"{len(combined_schedule)}"
    )

    print(
        "=" * 90
    )

# ============================================================
# EXPORT COMBINED MISSION SCHEDULE
# ============================================================

import csv
import os


def export_combined_schedule(
    combined_schedule,
    filename,
    station_name,
    station_latitude,
    station_longitude,
    observation_time,
    prediction_window_minutes,
    prediction_step_seconds,
    elevation_mask_deg
):
    """
    Export the combined multi-satellite mission
    schedule to a CSV file.
    """

    # --------------------------------------------------------
    # Create output directory if required
    # --------------------------------------------------------

    output_directory = os.path.dirname(
        filename
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Open CSV
    # --------------------------------------------------------

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        writer.writerow(
            [
                "Ground Station",
                station_name
            ]
        )

        writer.writerow(
            [
                "Station Latitude (deg)",
                station_latitude
            ]
        )

        writer.writerow(
            [
                "Station Longitude (deg)",
                station_longitude
            ]
        )

        writer.writerow(
            [
                "Prediction Start",
                observation_time.utc_strftime(
                    "%Y-%m-%d %H:%M:%S UTC"
                )
            ]
        )

        writer.writerow(
            [
                "Prediction Window (minutes)",
                prediction_window_minutes
            ]
        )

        writer.writerow(
            [
                "Prediction Step (seconds)",
                prediction_step_seconds
            ]
        )

        writer.writerow(
            [
                "Elevation Mask (deg)",
                elevation_mask_deg
            ]
        )

        writer.writerow([])

        # ----------------------------------------------------
        # Pass table header
        # ----------------------------------------------------

        writer.writerow(
            [
                "AOS",
                "Satellite",
                "Maximum Elevation (deg)",
                "Maximum Elevation Time",
                "LOS",
                "Duration (minutes)",
                "Elevation Mask (deg)"
            ]
        )

        # ----------------------------------------------------
        # Pass data
        # ----------------------------------------------------

        for pass_result in combined_schedule:

            writer.writerow(
                [
                    pass_result.aos_time.utc_strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                    pass_result.satellite_name,

                    f"{pass_result.max_elevation_deg:.2f}",

                    pass_result.max_elevation_time.utc_strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                    pass_result.los_time.utc_strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                    f"{pass_result.duration_minutes:.2f}",

                    f"{pass_result.elevation_mask_deg:.2f}"
                ]
            )


# ============================================================
# MISSION SCHEDULE STATISTICS
# ============================================================

def calculate_schedule_statistics(
    combined_schedule
):
    """
    Calculate overall statistics for the
    combined multi-satellite mission schedule.
    """

    # --------------------------------------------------------
    # Handle empty schedule
    # --------------------------------------------------------

    if not combined_schedule:

        return {
            "total_passes": 0,
            "total_satellites": 0,
            "average_duration_minutes": 0.0,
            "highest_elevation_deg": None,
            "longest_duration_minutes": None
        }

    # --------------------------------------------------------
    # Total passes
    # --------------------------------------------------------

    total_passes = len(
        combined_schedule
    )

    # --------------------------------------------------------
    # Unique satellites
    # --------------------------------------------------------

    satellite_names = set(
        pass_result.satellite_name
        for pass_result in combined_schedule
    )

    total_satellites = len(
        satellite_names
    )

    # --------------------------------------------------------
    # Average duration
    # --------------------------------------------------------

    total_duration_minutes = sum(
        pass_result.duration_minutes
        for pass_result in combined_schedule
    )

    average_duration_minutes = (
        total_duration_minutes
        / total_passes
    )

    # --------------------------------------------------------
    # Highest elevation
    # --------------------------------------------------------

    highest_elevation_pass = max(
        combined_schedule,
        key=lambda pass_result:
            pass_result.max_elevation_deg
    )

    highest_elevation_deg = (
        highest_elevation_pass
        .max_elevation_deg
    )

    # --------------------------------------------------------
    # Longest pass
    # --------------------------------------------------------

    longest_pass = max(
        combined_schedule,
        key=lambda pass_result:
            pass_result.duration_minutes
    )

    longest_duration_minutes = (
        longest_pass.duration_minutes
    )

    # --------------------------------------------------------
    # Return statistics
    # --------------------------------------------------------

    return {
        "total_passes":
            total_passes,

        "total_satellites":
            total_satellites,

        "average_duration_minutes":
            average_duration_minutes,

        "highest_elevation_deg":
            highest_elevation_deg,

        "longest_duration_minutes":
            longest_duration_minutes
    }

# ============================================================
# FIND NEXT UPCOMING PASS
# ============================================================

def find_next_upcoming_pass(
    combined_schedule,
    current_time
):
    """
    Find the first satellite pass whose AOS
    occurs at or after the current time.

    Skyfield Time objects are compared using
    their Julian date values.
    """

    # --------------------------------------------------------
    # Handle empty schedule
    # --------------------------------------------------------

    if not combined_schedule:

        return None

    # --------------------------------------------------------
    # Search chronologically
    # --------------------------------------------------------

    for pass_result in combined_schedule:

        if (
            pass_result.aos_time.tt
            >= current_time.tt
        ):

            return pass_result

    # --------------------------------------------------------
    # No future pass
    # --------------------------------------------------------

    return None

# ============================================================
# RANK SATELLITE PASSES
# ============================================================

def rank_passes_by_elevation(
    combined_schedule
):
    """
    Rank satellite passes from highest to
    lowest maximum elevation.
    """

    # --------------------------------------------------------
    # Handle empty schedule
    # --------------------------------------------------------

    if not combined_schedule:

        return []

    # --------------------------------------------------------
    # Sort by maximum elevation
    # --------------------------------------------------------

    ranked_passes = sorted(
        combined_schedule,
        key=lambda pass_result:
            pass_result.max_elevation_deg,
        reverse=True
    )

    return ranked_passes

# ============================================================
# PRINT PASS RANKING
# ============================================================

def print_pass_ranking(
    ranked_passes
):
    """
    Print satellite passes ranked by
    maximum elevation.
    """

    print(
        "\n" + "=" * 80
    )

    print(
        "                    PASS RANKING"
    )

    print(
        "=" * 80
    )

    # --------------------------------------------------------
    # Empty ranking
    # --------------------------------------------------------

    if not ranked_passes:

        print(
            "\nNo passes available for ranking."
        )

        print(
            "=" * 80
        )

        return

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print(
        f"{'RANK':<8}"
        f"{'SATELLITE':<22}"
        f"{'MAX ELEV.':>14}"
        f"{'DURATION':>14}"
    )

    print(
        "-" * 80
    )

    # --------------------------------------------------------
    # Ranking
    # --------------------------------------------------------

    for rank, pass_result in enumerate(
        ranked_passes,
        start=1
    ):

        print(
            f"{rank:<8}"
            f"{pass_result.satellite_name:<22}"
            f"{pass_result.max_elevation_deg:>12.2f}°"
            f"{pass_result.duration_minutes:>11.2f} min"
        )

    print(
        "=" * 80
    )