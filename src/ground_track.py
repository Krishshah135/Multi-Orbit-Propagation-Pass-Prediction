from skyfield.api import wgs84


def satellite_latlon(satellite, time):
    """
    Calculate the satellite's geographic latitude,
    longitude, and altitude at a given time.

    Parameters:
        satellite: Skyfield EarthSatellite object
        time: Skyfield Time object

    Returns:
        latitude_deg
        longitude_deg
        altitude_km
    """

    geocentric = satellite.at(time)

    geographic_position = (
        wgs84.geographic_position_of(geocentric)
    )

    latitude = geographic_position.latitude.degrees
    longitude = geographic_position.longitude.degrees
    altitude = geographic_position.elevation.km

    return latitude, longitude, altitude

def generate_ground_track(
    satellite,
    times
):
    """
    Generate latitude, longitude, and altitude
    for a sequence of times.

    Parameters:
        satellite: Skyfield EarthSatellite
        times: Skyfield Time array

    Returns:
        latitudes
        longitudes
        altitudes
    """

    geocentric = satellite.at(times)

    geographic_position = (
        wgs84.geographic_position_of(geocentric)
    )

    latitudes = geographic_position.latitude.degrees
    longitudes = geographic_position.longitude.degrees
    altitudes = geographic_position.elevation.km

    return (
        latitudes,
        longitudes,
        altitudes
    )