# ============================================================
# PREDICTION REPORT
# ============================================================


def _get_pass_value(
    pass_result,
    field_name
):
    """
    Read a value from either a PassResult object
    or a dictionary.
    """

    if isinstance(
        pass_result,
        dict
    ):
        return pass_result[field_name]

    return getattr(
        pass_result,
        field_name
    )


# ============================================================
# BUILD PREDICTION REPORT
# ============================================================

def build_prediction_report(
    pass_results
):
    """
    Build a summary report from predicted
    satellite passes.
    """

    # --------------------------------------------------------
    # No-pass condition
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
    # Highest elevation pass
    # --------------------------------------------------------

    highest_elevation_pass = max(
        pass_results,
        key=lambda result:
            _get_pass_value(
                result,
                "max_elevation_deg"
            )
    )

    # --------------------------------------------------------
    # Longest pass
    # --------------------------------------------------------

    longest_pass = max(
        pass_results,
        key=lambda result:
            _get_pass_value(
                result,
                "duration_minutes"
            )
    )

    # --------------------------------------------------------
    # Average duration
    # --------------------------------------------------------

    total_duration_minutes = sum(
        _get_pass_value(
            result,
            "duration_minutes"
        )
        for result in pass_results
    )

    average_duration_minutes = (
        total_duration_minutes
        / total_passes
    )

    # --------------------------------------------------------
    # Best pass
    # --------------------------------------------------------

    best_pass = highest_elevation_pass

    # --------------------------------------------------------
    # Return report
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


# ============================================================
# PRINT PREDICTION REPORT
# ============================================================

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
        f"Satellite            : "
        f"{_get_pass_value(best_pass, 'satellite_name')}"
    )

    print(
        f"Maximum Elevation    : "
        f"{_get_pass_value(best_pass, 'max_elevation_deg'):.2f}°"
    )

    print(
        f"Duration             : "
        f"{_get_pass_value(best_pass, 'duration_minutes'):.2f} minutes"
    )

    print(
        f"AOS                  : "
        f"{_get_pass_value(best_pass, 'aos_time')}"
    )

    print(
        f"MAX                  : "
        f"{_get_pass_value(best_pass, 'max_elevation_time')}"
    )

    print(
        f"LOS                  : "
        f"{_get_pass_value(best_pass, 'los_time')}"
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
        f"Satellite            : "
        f"{_get_pass_value(longest_pass, 'satellite_name')}"
    )

    print(
        f"Duration             : "
        f"{_get_pass_value(longest_pass, 'duration_minutes'):.2f} minutes"
    )

    print(
        f"Maximum Elevation    : "
        f"{_get_pass_value(longest_pass, 'max_elevation_deg'):.2f}°"
    )

    print(
        "=" * 60
    )