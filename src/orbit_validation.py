# ============================================================
# ORBIT VALIDATION
# ============================================================


def validate_orbital_parameters(
    analysis
):
    """
    Perform basic sanity checks on
    calculated orbital parameters.
    """

    errors = []

    warnings = []

    # --------------------------------------------------------
    # Semi-major axis
    # --------------------------------------------------------

    if analysis["semi_major_axis_km"] <= 0:

        errors.append(
            "Semi-major axis must be positive."
        )

    # --------------------------------------------------------
    # Eccentricity
    # --------------------------------------------------------

    eccentricity = (
        analysis["eccentricity"]
    )

    if eccentricity < 0:

        errors.append(
            "Eccentricity cannot be negative."
        )

    if eccentricity >= 1:

        warnings.append(
            "Orbit is not an elliptical Earth orbit."
        )

    # --------------------------------------------------------
    # Altitude
    # --------------------------------------------------------

    altitude = (
        analysis["altitude_km"]
    )

    if altitude < 0:

        warnings.append(
            "Calculated altitude is below "
            "Earth's reference radius."
        )

    # --------------------------------------------------------
    # Inclination
    # --------------------------------------------------------

    inclination = (
        analysis["inclination_deg"]
    )

    if inclination < 0 or inclination > 180:

        errors.append(
            "Inclination must be between "
            "0 and 180 degrees."
        )

    # --------------------------------------------------------
    # Period
    # --------------------------------------------------------

    if analysis["period_minutes"] <= 0:

        errors.append(
            "Orbital period must be positive."
        )

    # --------------------------------------------------------
    # Return results
    # --------------------------------------------------------

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }