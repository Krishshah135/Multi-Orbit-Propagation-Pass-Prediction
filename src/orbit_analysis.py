import math
import numpy as np


# ============================================================
# CONSTANTS
# ============================================================

# Earth's gravitational parameter
# km^3 / s^2
MU_EARTH = 398600.4418

# Earth's mean equatorial radius
# km
EARTH_RADIUS = 6378.137


# ============================================================
# ORBITAL ELEMENT EXTRACTION
# ============================================================

def extract_orbital_elements(satellite):
    """
    Extract key orbital elements from a Skyfield
    EarthSatellite.

    Skyfield's SGP4 model stores angular quantities
    internally in radians.

    Therefore:
        inclination -> degrees
        RAAN        -> degrees
        argument of perigee -> degrees
        mean anomaly -> degrees

    Mean motion is kept in radians/minute because it
    is converted separately to revolutions/day.
    """

    model = satellite.model

    elements = {
        "inclination_deg": np.degrees(
            float(model.inclo)
        ),

        "raan_deg": np.degrees(
            float(model.nodeo)
        ),

        "eccentricity": float(
            model.ecco
        ),

        "argument_of_perigee_deg": np.degrees(
            float(model.argpo)
        ),

        "mean_anomaly_deg": np.degrees(
            float(model.mo)
        ),

        "mean_motion_rad_per_min": float(
            model.no_kozai
        ),
    }

    return elements


# ============================================================
# MEAN MOTION
# ============================================================

def mean_motion_rev_per_day(
    mean_motion_rad_per_min
):
    """
    Convert mean motion from radians/minute
    to revolutions/day.
    """

    return (
        mean_motion_rad_per_min
        * 1440.0
        / (2.0 * math.pi)
    )


# ============================================================
# ORBITAL PERIOD
# ============================================================

def orbital_period_minutes(
    mean_motion_rev_day
):
    """
    Calculate orbital period from mean motion.

    Period = 1440 / mean_motion
    """

    if mean_motion_rev_day <= 0:
        raise ValueError(
            "Mean motion must be greater than zero."
        )

    return (
        1.0
        / mean_motion_rev_day
    ) * 1440.0


# ============================================================
# SEMI-MAJOR AXIS
# ============================================================

def semi_major_axis(
    period_minutes
):
    """
    Calculate approximate semi-major axis
    using the two-body orbital relationship.

        T = 2*pi*sqrt(a^3 / mu)

    Therefore:

        a = (mu*T^2 / 4*pi^2)^(1/3)

    Returns:
        Semi-major axis in km.
    """

    period_seconds = (
        period_minutes * 60.0
    )

    a = (
        MU_EARTH
        * period_seconds**2
        / (4.0 * math.pi**2)
    ) ** (1.0 / 3.0)

    return a


# ============================================================
# ORBITAL ALTITUDE
# ============================================================

def approximate_altitude(
    period_minutes
):
    """
    Calculate approximate orbital altitude
    from the semi-major axis.

    Returns:
        Altitude in km.
    """

    a = semi_major_axis(
        period_minutes
    )

    return (
        a - EARTH_RADIUS
    )


# ============================================================
# PERIGEE RADIUS
# ============================================================

def perigee_radius(
    semi_major_axis_km,
    eccentricity
):
    """
    Calculate distance from Earth's center
    at perigee.

        rp = a(1-e)
    """

    return (
        semi_major_axis_km
        * (1.0 - eccentricity)
    )


# ============================================================
# APOGEE RADIUS
# ============================================================

def apogee_radius(
    semi_major_axis_km,
    eccentricity
):
    """
    Calculate distance from Earth's center
    at apogee.

        ra = a(1+e)
    """

    return (
        semi_major_axis_km
        * (1.0 + eccentricity)
    )


# ============================================================
# VIS-VIVA VELOCITY
# ============================================================

def velocity_from_vis_viva(
    radius_km,
    semi_major_axis_km
):
    """
    Calculate orbital velocity using the
    vis-viva equation.

        v = sqrt(mu * (2/r - 1/a))

    Returns:
        Velocity in km/s.
    """

    velocity_squared = (
        MU_EARTH
        * (
            2.0 / radius_km
            - 1.0 / semi_major_axis_km
        )
    )

    return math.sqrt(
        velocity_squared
    )


# ============================================================
# PERIGEE VELOCITY
# ============================================================

def perigee_velocity(
    semi_major_axis_km,
    eccentricity
):
    """
    Calculate orbital velocity at perigee.
    """

    rp = perigee_radius(
        semi_major_axis_km,
        eccentricity
    )

    return velocity_from_vis_viva(
        rp,
        semi_major_axis_km
    )


# ============================================================
# APOGEE VELOCITY
# ============================================================

def apogee_velocity(
    semi_major_axis_km,
    eccentricity
):
    """
    Calculate orbital velocity at apogee.
    """

    ra = apogee_radius(
        semi_major_axis_km,
        eccentricity
    )

    return velocity_from_vis_viva(
        ra,
        semi_major_axis_km
    )


# ============================================================
# COMPLETE ORBIT ANALYSIS
# ============================================================

def analyze_orbit(satellite):
    """
    Perform complete orbital analysis.

    Returns a dictionary containing:

    - Inclination
    - RAAN
    - Eccentricity
    - Argument of perigee
    - Mean anomaly
    - Mean motion
    - Orbital period
    - Semi-major axis
    - Altitude
    - Perigee/apogee radius
    - Perigee/apogee altitude
    - Perigee/apogee velocity
    """

    # --------------------------------------------------------
    # Extract TLE orbital elements
    # --------------------------------------------------------

    elements = extract_orbital_elements(
        satellite
    )

    # --------------------------------------------------------
    # Mean motion
    # --------------------------------------------------------

    mean_motion = (
        mean_motion_rev_per_day(
            elements[
                "mean_motion_rad_per_min"
            ]
        )
    )

    # --------------------------------------------------------
    # Orbital period
    # --------------------------------------------------------

    period = (
        orbital_period_minutes(
            mean_motion
        )
    )

    # --------------------------------------------------------
    # Semi-major axis
    # --------------------------------------------------------

    sma = semi_major_axis(
        period
    )

    # --------------------------------------------------------
    # Approximate altitude
    # --------------------------------------------------------

    altitude = approximate_altitude(
        period
    )

    # --------------------------------------------------------
    # Eccentricity
    # --------------------------------------------------------

    eccentricity = (
        elements[
            "eccentricity"
        ]
    )

    # --------------------------------------------------------
    # Perigee / apogee radius
    # --------------------------------------------------------

    rp = perigee_radius(
        sma,
        eccentricity
    )

    ra = apogee_radius(
        sma,
        eccentricity
    )

    # --------------------------------------------------------
    # Perigee / apogee velocity
    # --------------------------------------------------------

    vp = perigee_velocity(
        sma,
        eccentricity
    )

    va = apogee_velocity(
        sma,
        eccentricity
    )

    # --------------------------------------------------------
    # Final results
    # --------------------------------------------------------

    return {
        "inclination_deg":
            elements[
                "inclination_deg"
            ],

        "raan_deg":
            elements[
                "raan_deg"
            ],

        "eccentricity":
            eccentricity,

        "argument_of_perigee_deg":
            elements[
                "argument_of_perigee_deg"
            ],

        "mean_anomaly_deg":
            elements[
                "mean_anomaly_deg"
            ],

        "mean_motion_rev_day":
            mean_motion,

        "period_minutes":
            period,

        "semi_major_axis_km":
            sma,

        "altitude_km":
            altitude,

        "perigee_radius_km":
            rp,

        "apogee_radius_km":
            ra,

        "perigee_altitude_km":
            rp - EARTH_RADIUS,

        "apogee_altitude_km":
            ra - EARTH_RADIUS,

        "perigee_velocity_km_s":
            vp,

        "apogee_velocity_km_s":
            va,
    }