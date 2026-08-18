# ============================================================
# PREDICTION REPORT
# ============================================================


def build_prediction_report(
    pass_results
):
    """
    Build a summary report from predicted
    satellite passes.
    """

    # --------------------------------------------------------
    # Handle no-pass condition
    # --------------------------------------------------------

    if not pass_results:

        return {
            "total_passes": 0,
            "best_pass": None,
            "highest_elevation": None,
            "longest_pass": None,
            "average_duration_minutes": 0.0
        }

    # --------------------------------------------------------
    # Total number of passes
    # --------------------------------------------------------

    total_passes = len(
        pass_results
    )

    # --------------------------------------------------------
    # Find highest-elevation pass
    # --------------------------------------------------------

    highest_elevation_pass = max(
        pass_results,
        key=lambda result:
            result["max_elevation_deg"]
    )

    # --------------------------------------------------------
    # Find longest pass
    # --------------------------------------------------------

    longest_pass = max(
        pass_results,
        key=lambda result:
            result["duration_seconds"]
    )

    # --------------------------------------------------------
    # Calculate average duration
    # --------------------------------------------------------

    total_duration_seconds = sum(
        result["duration_seconds"]
        for result in pass_results
    )

    average_duration_minutes = (
        total_duration_seconds
        / total_passes
        / 60
    )

    # --------------------------------------------------------
    # Best pass
    #
    # For now, highest maximum elevation
    # is our definition of "best".
    # --------------------------------------------------------

    best_pass = highest_elevation_pass

    # --------------------------------------------------------
    # Return structured report
    # --------------------------------------------------------

    return {
        "total_passes":
            total_passes,

        "best_pass":
            best_pass,

        "highest_elevation":
            highest_elevation_pass,

        "longest_pass":
            longest_pass,

        "average_duration_minutes":
            average_duration_minutes
    }


def print_prediction_report(
    report
):
    """
    Print a human-readable prediction report.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "                 PREDICTION REPORT"
    )

    print(
        "=" * 60
    )

    # --------------------------------------------------------
    # Total passes
    # --------------------------------------------------------

    print(
        f"Total Passes          : "
        f"{report['total_passes']}"
    )

    # --------------------------------------------------------
    # No-pass condition
    # --------------------------------------------------------

    if report["total_passes"] == 0:

        print(
            "\nNo visible passes detected "
            "during the prediction window."
        )

        print(
            "=" * 60
        )

        return

    # --------------------------------------------------------
    # Average duration
    # --------------------------------------------------------

    print(
        f"Average Pass Duration : "
        f"{report['average_duration_minutes']:.2f} minutes"
    )

    # --------------------------------------------------------
    # Best pass
    # --------------------------------------------------------

    best_pass = report["best_pass"]

    print(
        "\nBEST PASS"
    )

    print(
        "-" * 60
    )

    print(
        f"Maximum Elevation    : "
        f"{best_pass['max_elevation_deg']:.2f}°"
    )

    print(
        f"Duration             : "
        f"{best_pass['duration_seconds'] / 60:.2f} minutes"
    )

    print(
        f"AOS                  : "
        f"{best_pass['aos_time']}"
    )

    print(
        f"MAX                  : "
        f"{best_pass['max_elevation_time']}"
    )

    print(
        f"LOS                  : "
        f"{best_pass['los_time']}"
    )

    # --------------------------------------------------------
    # Longest pass
    # --------------------------------------------------------

    longest_pass = (
        report["longest_pass"]
    )

    print(
        "\nLONGEST PASS"
    )

    print(
        "-" * 60
    )

    print(
        f"Duration             : "
        f"{longest_pass['duration_seconds'] / 60:.2f} minutes"
    )

    print(
        f"Maximum Elevation    : "
        f"{longest_pass['max_elevation_deg']:.2f}°"
    )

    print(
        "=" * 60
    )