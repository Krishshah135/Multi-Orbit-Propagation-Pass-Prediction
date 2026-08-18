from src.tle_loader import (
    load_satellite_from_file
)

from src.orbit_analysis import (
    analyze_orbit
)

from src.orbit_classification import (
    classify_orbit
)

from src.orbit_validation import (
    validate_orbital_parameters
)

from src.satellite_profile import (
    build_satellite_profile,
    print_satellite_profile
)


# ============================================================
# LOAD SATELLITE
# ============================================================

satellites = load_satellite_from_file(
    "data/tle/iss.tle"
)

satellite = satellites[0]


# ============================================================
# ORBIT ANALYSIS
# ============================================================

analysis = analyze_orbit(
    satellite
)


# ============================================================
# ORBIT CLASSIFICATION
# ============================================================

classification = classify_orbit(
    analysis["altitude_km"],
    analysis["period_minutes"],
    analysis["eccentricity"],
    analysis["inclination_deg"]
)


# ============================================================
# ORBIT VALIDATION
# ============================================================

validation = validate_orbital_parameters(
    analysis
)


# ============================================================
# BUILD PROFILE
# ============================================================

profile = build_satellite_profile(
    satellite,
    analysis,
    classification,
    validation,
    "data/tle/iss.tle"
)


# ============================================================
# DISPLAY PROFILE
# ============================================================

print_satellite_profile(
    profile
)


# ============================================================
# BASIC TESTS
# ============================================================

assert (
    profile["name"]
    == satellite.name
)

assert (
    profile["validation"]["valid"]
    is True
)

assert (
    "orbital_elements"
    in profile
)

assert (
    "derived_parameters"
    in profile
)

assert (
    "classification"
    in profile
)


print(
    "\nSatellite profile test passed."
)