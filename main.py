from src.tle_loader import load_satellites
from src.orbit_analysis import analyze_orbit


# Load satellite data from CelesTrak
satellites = load_satellites()


# Find the ISS
iss = next(
    satellite
    for satellite in satellites
    if satellite.name == "ISS (ZARYA)"
)


# Perform orbital analysis
analysis = analyze_orbit(iss)


# Display results
print("=" * 60)
print("                 ORBITAL ANALYSIS")
print("=" * 60)

print(f"\nSatellite          : {iss.name}")

print("\nORBITAL ELEMENTS")
print("-" * 60)

print(
    f"Inclination        : "
    f"{analysis['inclination_deg']:.4f}°"
)

print(
    f"RAAN               : "
    f"{analysis['raan_deg']:.4f}°"
)

print(
    f"Eccentricity       : "
    f"{analysis['eccentricity']:.7f}"
)

print(
    f"Argument of Perigee: "
    f"{analysis['argument_of_perigee_deg']:.4f}°"
)

print(
    f"Mean Anomaly       : "
    f"{analysis['mean_anomaly_deg']:.4f}°"
)

print(
    f"Mean Motion        : "
    f"{analysis['mean_motion_rev_day']:.4f} rev/day"
)


print("\nDERIVED ORBITAL PARAMETERS")
print("-" * 60)

print(
    f"Orbital Period     : "
    f"{analysis['period_minutes']:.2f} min"
)

print(
    f"Semi-Major Axis    : "
    f"{analysis['semi_major_axis_km']:.2f} km"
)

print(
    f"Approx. Altitude   : "
    f"{analysis['altitude_km']:.2f} km"
)


print("\nPERIGEE / APOGEE")
print("-" * 60)

print(
    f"Perigee Radius     : "
    f"{analysis['perigee_radius_km']:.2f} km"
)

print(
    f"Apogee Radius      : "
    f"{analysis['apogee_radius_km']:.2f} km"
)

print(
    f"Perigee Altitude   : "
    f"{analysis['perigee_altitude_km']:.2f} km"
)

print(
    f"Apogee Altitude    : "
    f"{analysis['apogee_altitude_km']:.2f} km"
)


print("\nORBITAL VELOCITY")
print("-" * 60)

print(
    f"Perigee Velocity   : "
    f"{analysis['perigee_velocity_km_s']:.4f} km/s"
)

print(
    f"Apogee Velocity     : "
    f"{analysis['apogee_velocity_km_s']:.4f} km/s"
)


print("=" * 60)