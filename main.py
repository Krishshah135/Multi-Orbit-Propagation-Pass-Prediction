from src.tle_loader import load_satellites
from src.propagator import propagate_satellite

satellites = load_satellites()

iss = next(s for s in satellites if s.name == "ISS (ZARYA)")

time, position = propagate_satellite(iss)

print(f"Satellite : {iss.name}")
print(f"UTC Time  : {time.utc_iso()}")

print(f"X = {position[0]:.2f} km")
print(f"Y = {position[1]:.2f} km")
print(f"Z = {position[2]:.2f} km")