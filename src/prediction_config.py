# ============================================================
# PREDICTION CONFIGURATION
# ============================================================


def create_prediction_config(
    duration_minutes=720,
    step_seconds=10,
    elevation_mask_deg=10.0
):
    """
    Create a prediction configuration.

    Parameters
    ----------
    duration_minutes : int or float
        Total prediction window.

    step_seconds : int or float
        Time resolution used during propagation.

    elevation_mask_deg : float
        Minimum elevation required for
        a satellite to be considered visible.
    """

    # --------------------------------------------------------
    # Validate prediction duration
    # --------------------------------------------------------

    if duration_minutes <= 0:

        raise ValueError(
            "Prediction duration must "
            "be greater than zero."
        )

    # --------------------------------------------------------
    # Validate time step
    # --------------------------------------------------------

    if step_seconds <= 0:

        raise ValueError(
            "Prediction step must "
            "be greater than zero."
        )

    # --------------------------------------------------------
    # Validate elevation mask
    # --------------------------------------------------------

    if (
        elevation_mask_deg < 0
        or elevation_mask_deg > 90
    ):

        raise ValueError(
            "Elevation mask must be "
            "between 0 and 90 degrees."
        )

    # --------------------------------------------------------
    # Return configuration
    # --------------------------------------------------------

    return {
        "duration_minutes":
            duration_minutes,

        "step_seconds":
            step_seconds,

        "elevation_mask_deg":
            elevation_mask_deg
    }


def print_prediction_config(
    config
):
    """
    Display the active prediction
    configuration.
    """

    print(
        "\nPREDICTION CONFIGURATION"
    )

    print(
        "-" * 60
    )

    print(
        f"Prediction Duration : "
        f"{config['duration_minutes']} minutes"
    )

    print(
        f"Time Step           : "
        f"{config['step_seconds']} seconds"
    )

    print(
        f"Elevation Mask      : "
        f"{config['elevation_mask_deg']:.1f}°"
    )