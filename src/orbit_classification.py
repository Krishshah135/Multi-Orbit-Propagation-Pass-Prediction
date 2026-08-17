
# ============================================================
# ORBIT CLASSIFICATION
# ============================================================


def classify_by_altitude(
    altitude_km
):
    """
    Classify an orbit based on
    approximate altitude above Earth.

    These are broad engineering categories,
    not strict mission-specific definitions.
    """

    if altitude_km < 2000:

        return "LEO"

    elif altitude_km < 35786:

        return "MEO"

    elif altitude_km < 40000:

        return "GEO / GEO-LIKE"

    else:

        return "HIGH-EARTH / HEO"


def classify_by_period(
    period_minutes
):
    """
    Provide an additional orbit classification
    based on orbital period.
    """

    if period_minutes < 128:

        return "Low-period orbit"

    elif period_minutes < 1440:

        return "Medium-period orbit"

    elif period_minutes < 1500:

        return "Geosynchronous-period orbit"

    else:

        return "Long-period orbit"


def classify_orbit(
    altitude_km,
    period_minutes,
    eccentricity,
    inclination_deg
):
    """
    Return a complete engineering
    classification of an orbit.
    """

    altitude_class = classify_by_altitude(
        altitude_km
    )

    period_class = classify_by_period(
        period_minutes
    )

    if eccentricity < 0.01:

        eccentricity_class = (
            "Near-circular"
        )

    elif eccentricity < 0.1:

        eccentricity_class = (
            "Low-eccentricity"
        )

    elif eccentricity < 0.5:

        eccentricity_class = (
            "Moderately-eccentric"
        )

    else:

        eccentricity_class = (
            "Highly-eccentric"
        )

    if inclination_deg < 10:

        inclination_class = (
            "Near-equatorial"
        )

    elif inclination_deg < 45:

        inclination_class = (
            "Moderate-inclination"
        )

    elif inclination_deg < 90:

        inclination_class = (
            "High-inclination"
        )

    else:

        inclination_class = (
            "Polar / Retrograde"
        )

    return {
        "altitude_class": altitude_class,
        "period_class": period_class,
        "eccentricity_class": eccentricity_class,
        "inclination_class": inclination_class
    }