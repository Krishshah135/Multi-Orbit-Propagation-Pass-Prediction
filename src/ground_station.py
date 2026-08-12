import numpy as np

from skyfield.api import wgs84
from skyfield.framelib import itrs


def create_ground_station(
    latitude_deg,
    longitude_deg,
    elevation_m=0.0
):
    """
    Create a WGS84 ground station.

    Parameters:
        latitude_deg: Ground station latitude [degrees]
        longitude_deg: Ground station longitude [degrees]
        elevation_m: Ground station elevation [meters]

    Returns:
        Skyfield geographic position
    """

    return wgs84.latlon(
        latitude_deg,
        longitude_deg,
        elevation_m=elevation_m
    )


def get_ecef_position(position):
    """
    Convert a Skyfield position to
    Earth-Centered Earth-Fixed (ECEF)
    coordinates.

    Returns:
        numpy array [X, Y, Z] in km
    """

    return position.frame_xyz(itrs).km


def calculate_los_vector(
    satellite_position_ecef,
    station_position_ecef
):
    """
    Calculate the line-of-sight vector
    from the ground station to the satellite.

    LOS = Satellite position - Station position

    Returns:
        LOS vector in ECEF coordinates [km]
    """

    return (
        satellite_position_ecef
        - station_position_ecef
    )


def calculate_range(los_vector):
    """
    Calculate slant range between
    ground station and satellite.

    Returns:
        Range in km
    """

    return np.linalg.norm(los_vector)


def ecef_to_enu(
    los_vector,
    latitude_deg,
    longitude_deg
):
    """
    Convert an ECEF line-of-sight vector
    into the local East-North-Up (ENU) frame.

    Returns:
        east, north, up [km]
    """

    latitude = np.radians(latitude_deg)
    longitude = np.radians(longitude_deg)

    x = los_vector[0]
    y = los_vector[1]
    z = los_vector[2]

    east = (
        -np.sin(longitude) * x
        + np.cos(longitude) * y
    )

    north = (
        -np.sin(latitude)
        * np.cos(longitude)
        * x

        - np.sin(latitude)
        * np.sin(longitude)
        * y

        + np.cos(latitude)
        * z
    )

    up = (
        np.cos(latitude)
        * np.cos(longitude)
        * x

        + np.cos(latitude)
        * np.sin(longitude)
        * y

        + np.sin(latitude)
        * z
    )

    return east, north, up


def calculate_elevation(
    east,
    north,
    up
):
    """
    Calculate satellite elevation angle
    above the local horizon.

    Returns:
        Elevation angle [degrees]
    """

    horizontal_range = np.sqrt(
        east**2 + north**2
    )

    elevation = np.degrees(
        np.arctan2(
            up,
            horizontal_range
        )
    )

    return elevation


def calculate_azimuth(
    east,
    north
):
    """
    Calculate satellite azimuth.

    Azimuth convention:

        0°   = North
        90°  = East
        180° = South
        270° = West

    Returns:
        Azimuth [0, 360) degrees
    """

    azimuth = np.degrees(
        np.arctan2(
            east,
            north
        )
    )

    return azimuth % 360


def observe_satellite(
    satellite,
    time,
    station,
    latitude_deg,
    longitude_deg
):
    """
    Calculate the satellite's observation
    parameters from a ground station.

    Returns:
        Dictionary containing:

        range_km
        azimuth_deg
        elevation_deg
    """

    # --------------------------------------------------
    # 1. Get satellite position
    # --------------------------------------------------

    satellite_position = satellite.at(time)

    satellite_ecef = get_ecef_position(
        satellite_position
    )


    # --------------------------------------------------
    # 2. Get ground station ECEF position
    # --------------------------------------------------

    station_ecef = (
        station
        .at(time)
        .frame_xyz(itrs)
        .km
    )


    # --------------------------------------------------
    # 3. Calculate line-of-sight vector
    # --------------------------------------------------

    los_vector = calculate_los_vector(
        satellite_ecef,
        station_ecef
    )


    # --------------------------------------------------
    # 4. Calculate range
    # --------------------------------------------------

    range_km = calculate_range(
        los_vector
    )


    # --------------------------------------------------
    # 5. Convert LOS from ECEF to ENU
    # --------------------------------------------------

    east, north, up = ecef_to_enu(
        los_vector,
        latitude_deg,
        longitude_deg
    )


    # --------------------------------------------------
    # 6. Calculate elevation
    # --------------------------------------------------

    elevation_deg = calculate_elevation(
        east,
        north,
        up
    )


    # --------------------------------------------------
    # 7. Calculate azimuth
    # --------------------------------------------------

    azimuth_deg = calculate_azimuth(
        east,
        north
    )


    # --------------------------------------------------
    # 8. Return observation
    # --------------------------------------------------

    return {
        "range_km": range_km,
        "azimuth_deg": azimuth_deg,
        "elevation_deg": elevation_deg
    }
def validate_with_skyfield(
    satellite,
    time,
    station
):
    """
    Calculate satellite observation parameters
    using Skyfield's built-in altaz() method.

    This is used only as an independent
    validation reference.
    """

    # Calculate satellite position relative
    # to the ground station

    difference = satellite - station

    topocentric = difference.at(time)

    # Convert directly to altitude,
    # azimuth and distance

    altitude, azimuth, distance = (
        topocentric.altaz()
    )

    return {
        "range_km": distance.km,
        "azimuth_deg": azimuth.degrees,
        "elevation_deg": altitude.degrees
    }