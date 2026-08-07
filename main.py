from skyfield.api import load

ts = load.timescale()

stations_url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle"

satellites = load.tle_file(stations_url)

iss = next(s for s in satellites if s.name == "ISS (ZARYA)")

t = ts.now()

geocentric = iss.at(t)

position = geocentric.position.km

print(f"Satellite : {iss.name}")
print(f"UTC Time  : {t.utc_iso()}")

print("\nPosition (ECI)")

print(f"X = {position[0]:.2f} km")
print(f"Y = {position[1]:.2f} km")
print(f"Z = {position[2]:.2f} km")