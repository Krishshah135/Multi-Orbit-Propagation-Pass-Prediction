import math


# Earth's gravitational parameter
# km^3 / s^2
MU_EARTH = 398600.4418

# Earth's mean equatorial radius
# km
EARTH_RADIUS = 6378.137


def extract_orbital_elements(satellite):
    """
    Extract key orbital elements from a Skyfield EarthSatellite.
    """

    model = satellite.model

    elements = {
        "inclination_deg": model.inclo,
        "raan_deg": model.nodeo,
        "eccentricity": model.ecco,
        "argument_of_perigee_deg": model.argpo,
        "mean_anomaly_deg": model.mo,
        "mean_motion_rad_per_min": model.no_kozai,
    }

    return elements


def mean_motion_rev_per_day(mean_motion_rad_per_min):
    """
    Convert mean motion from radians/minute
    to revolutions/day.
    """

    return (
        mean_motion_rad_per_min
        * 1440
        / (2 * math.pi)
    )


def orbital_period_minutes(mean_motion_rev_day):
    """
    Calculate orbital period from mean motion.
    """

    return (1 / mean_motion_rev_day) * 1440


def semi_major_axis(period_minutes):
    """
    Calculate approximate semi-major axis
    using the two-body orbital relationship.
    """

    period_seconds = period_minutes * 60

    a = (
        MU_EARTH * period_seconds**2
        / (4 * math.pi**2)
    ) ** (1 / 3)

    return a


def approximate_altitude(period_minutes):
    """
    Calculate approximate orbital altitude.
    """

    a = semi_major_axis(period_minutes)

    return a - EARTH_RADIUS


def perigee_radius(semi_major_axis_km, eccentricity):
    """
    Calculate distance from Earth's center at perigee.
    """

    return semi_major_axis_km * (1 - eccentricity)


def apogee_radius(semi_major_axis_km, eccentricity):
    """
    Calculate distance from Earth's center at apogee.
    """

    return semi_major_axis_km * (1 + eccentricity)


def velocity_from_vis_viva(radius_km, semi_major_axis_km):
    """
    Calculate orbital velocity using the vis-viva equation.

    v = sqrt(mu * (2/r - 1/a))

    Returns velocity in km/s.
    """

    return math.sqrt(
        MU_EARTH
        * (
            2 / radius_km
            - 1 / semi_major_axis_km
        )
    )


def perigee_velocity(semi_major_axis_km, eccentricity):
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


def apogee_velocity(semi_major_axis_km, eccentricity):
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


def analyze_orbit(satellite):
    """
    Perform complete orbital analysis.
    """

    elements = extract_orbital_elements(satellite)

    mean_motion = mean_motion_rev_per_day(
        elements["mean_motion_rad_per_min"]
    )

    period = orbital_period_minutes(
        mean_motion
    )

    sma = semi_major_axis(period)

    altitude = approximate_altitude(period)

    eccentricity = elements["eccentricity"]

    rp = perigee_radius(
        sma,
        eccentricity
    )

    ra = apogee_radius(
        sma,
        eccentricity
    )

    vp = perigee_velocity(
        sma,
        eccentricity
    )

    va = apogee_velocity(
        sma,
        eccentricity
    )

    return {
        "inclination_deg":
            elements["inclination_deg"],

        "raan_deg":
            elements["raan_deg"],

        "eccentricity":
            eccentricity,

        "argument_of_perigee_deg":
            elements["argument_of_perigee_deg"],

        "mean_anomaly_deg":
            elements["mean_anomaly_deg"],

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