from src.satellite_catalog import (
    load_satellite_catalog,
    print_satellite_catalog,
    select_satellite
)


# ============================================================
# LOAD SATELLITE CATALOG
# ============================================================

catalog = load_satellite_catalog(
    "data/tle"
)


# ============================================================
# DISPLAY AVAILABLE SATELLITES
# ============================================================

print_satellite_catalog(
    catalog
)


# ============================================================
# TEST SATELLITE SELECTION
# ============================================================

satellite = select_satellite(
    catalog,
    1
)


# ============================================================
# DISPLAY SELECTED SATELLITE
# ============================================================

print("\nSELECTED SATELLITE")

print("-" * 60)

print(
    f"Name     : {satellite.name}"
)

print(
    f"Catalog  : Successfully selected"
)

print("-" * 60)