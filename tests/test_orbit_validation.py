from src.orbit_analysis import (
    analyze_orbit
)

from src.tle_loader import (
    load_satellite_from_file
)

from src.orbit_validation import (
    validate_orbital_parameters
)


# ============================================================
# LOAD ISS
# ============================================================

satellites = load_satellite_from_file(
    "data/tle/iss.tle"
)

satellite = satellites[0]


# ============================================================
# ANALYZE ORBIT
# ============================================================

analysis = analyze_orbit(
    satellite
)


# ============================================================
# VALIDATE
# ============================================================

validation = validate_orbital_parameters(
    analysis
)


# ============================================================
# DISPLAY
# ============================================================

print("\nORBIT VALIDATION")

print("-" * 60)

print(
    f"Valid : "
    f"{validation['valid']}"
)


if validation["errors"]:

    print("\nERRORS:")

    for error in validation["errors"]:

        print(
            f"- {error}"
        )


if validation["warnings"]:

    print("\nWARNINGS:")

    for warning in validation["warnings"]:

        print(
            f"- {warning}"
        )


print("-" * 60)


assert validation["valid"] is True

print(
    "Orbit validation test passed."
)