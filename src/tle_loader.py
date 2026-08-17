import requests
from skyfield.api import EarthSatellite, load
from skyfield.api import load

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

    response = requests.get(url, timeout=60)
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
def load_satellite_from_file(filepath):
    """
    Load satellites from a local 3-line TLE file.

    Expected format:

        Satellite Name
        TLE Line 1
        TLE Line 2
    """

    with open(filepath, "r") as file:
        lines = [
            line.strip()
            for line in file
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

        # Preserve the original TLE
        satellite.tle_line1 = line1
        satellite.tle_line2 = line2

        satellites.append(satellite)

    return satellites

def load_satellite_from_tle(filename):
    """
    Load a satellite from a local TLE file.

    The TLE file must contain:

    Line 1
    Line 2

    optionally preceded by a satellite name.
    """

    satellites = load.tle_file(
        filename
    )

    if not satellites:
        raise ValueError(
            f"No satellites found in {filename}"
        )

    return satellites[0]