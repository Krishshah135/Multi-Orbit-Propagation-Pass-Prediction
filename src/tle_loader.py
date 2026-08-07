from skyfield.api import load

def load_satellites(group="stations"):
    """
    Load satellites from CelesTrak.

    Parameters:
        group (str): CelesTrak satellite group

    Returns:
        list: Skyfield EarthSatellite objects
    """

    url = f"https://celestrak.org/NORAD/elements/gp.php?GROUP={group}&FORMAT=tle"

    satellites = load.tle_file(url)

    return satellites