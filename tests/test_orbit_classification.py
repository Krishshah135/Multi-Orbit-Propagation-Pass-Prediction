from src.orbit_classification import (
    classify_orbit
)


# ============================================================
# TEST ISS-LIKE ORBIT
# ============================================================

result = classify_orbit(
    altitude_km=400,
    period_minutes=92,
    eccentricity=0.001,
    inclination_deg=51.6
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("\nORBIT CLASSIFICATION TEST")

print("-" * 60)

print(
    f"Altitude Class     : "
    f"{result['altitude_class']}"
)

print(
    f"Period Class       : "
    f"{result['period_class']}"
)

print(
    f"Eccentricity Class : "
    f"{result['eccentricity_class']}"
)

print(
    f"Inclination Class  : "
    f"{result['inclination_class']}"
)

print("-" * 60)


# ============================================================
# BASIC ASSERTIONS
# ============================================================

assert (
    result["altitude_class"]
    == "LEO"
)

assert (
    result["eccentricity_class"]
    == "Near-circular"
)

assert (
    result["inclination_class"]
    == "High-inclination"
)


print(
    "All orbit classification tests passed."
)