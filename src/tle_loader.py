import requests
from skyfield.api import EarthSatellite, load


def load_satellites(group="stations"):
    """
    Download TLE data from CelesTrak and create Skyfield
    EarthSatellite objects.

    Returns:
        list: EarthSatellite objects
    """

    url = (
        f"https://celestrak.org/NORAD/elements/"
        f"gp.php?GROUP={group}&FORMAT=tle"
    )

    response = requests.get(url, timeout=15)
    response.raise_for_status()

    lines = [
        line.strip()
        for line in response.text.splitlines()
        if line.strip()
    ]

    ts = load.timescale()

    satellites = []

    for i in range(0, len(lines), 3):

        name = lines[i]
        line1 = lines[i + 1]
        line2 = lines[i + 2]

        satellite = EarthSatellite(
            line1,
            line2,
            name,
            ts
        )

        # Preserve original TLE data
        satellite.tle_line1 = line1
        satellite.tle_line2 = line2

        satellites.append(satellite)

    return satellites