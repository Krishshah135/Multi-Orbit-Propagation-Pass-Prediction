from skyfield.api import load

from src.satellite_catalog import (
    load_satellite_catalog
)

from src.ground_station import (
    create_ground_station
)

from src.prediction_config import (
    create_prediction_config
)

from src.multi_satellite_prediction import (
    predict_all_satellites
)


# ============================================================
# LOAD CATALOG
# ============================================================

catalog = load_satellite_catalog(
    "data/tle"
)


# ============================================================
# LOAD TIMESCALE
# ============================================================

ts = load.timescale()


# ============================================================
# OBSERVATION TIME
# ============================================================

observation_time = ts.now()


# ============================================================
# GROUND STATION
# ============================================================

station_latitude = 13.0827
station_longitude = 80.2707
station_elevation = 0.0

station = create_ground_station(
    station_latitude,
    station_longitude,
    station_elevation
)


# ============================================================
# PREDICTION CONFIGURATION
# ============================================================

prediction_config = create_prediction_config(
    duration_minutes=180,
    step_seconds=10,
    elevation_mask_deg=10.0
)


# ============================================================
# RUN ALL SATELLITE PREDICTIONS
# ============================================================

all_predictions = (
    predict_all_satellites(
        ts,
        catalog,
        station,
        station_latitude,
        station_longitude,
        observation_time,
        prediction_config
    )
)


# ============================================================
# BASIC TESTS
# ============================================================

assert (
    len(all_predictions)
    == len(catalog)
)


for satellite_name, prediction in (
    all_predictions.items()
):

    assert (
        prediction["satellite"]
        is not None
    )

    assert (
        "pass_results"
        in prediction
    )

    assert (
        "prediction_report"
        in prediction
    )


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print(
    "\n" + "=" * 60
)

print(
    "MULTI-SATELLITE PREDICTION TEST"
)

print(
    "=" * 60
)

for satellite_name, prediction in (
    all_predictions.items()
):

    print(
        f"{satellite_name:25}"
        f"Passes: "
        f"{len(prediction['pass_results'])}"
    )


print(
    "\nMulti-satellite prediction "
    "test passed."
)