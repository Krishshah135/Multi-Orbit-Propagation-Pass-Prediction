from skyfield.api import load

ts = load.timescale()

def propagate_satellite(satellite):
    """
    Propagate satellite to current UTC time.

    Returns:
        Position vector in kilometers.
    """

    t = ts.now()

    geocentric = satellite.at(t)

    return t, geocentric.position.km