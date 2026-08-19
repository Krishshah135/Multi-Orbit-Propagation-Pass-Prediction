import numpy as np

from src.satellite_catalog import (
    load_satellite_catalog,
    print_satellite_catalog,
    select_satellite
)

from src.orbit_analysis import analyze_orbit

from skyfield.api import load

from src.visualization import (
    plot_ground_track,
    plot_ground_track_map
)

from src.ground_track import (
    satellite_latlon,
    generate_ground_track
)

from src.ground_station import (
    create_ground_station,
    observe_satellite,
    validate_with_skyfield
)

from src.pass_prediction import (
    generate_prediction_times,
    calculate_elevation_profile,
    find_visibility_intervals,
    find_max_elevation,
    refine_pass_times,
    refine_max_elevation,
    build_pass_results,
    print_pass_summary,
    plot_elevation_profile,
    export_passes_to_csv
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

from src.prediction_config import (
    create_prediction_config,
    print_prediction_config
)

from src.prediction_report import (
    build_prediction_report,
    print_prediction_report
)

from src.multi_satellite_prediction import (
    predict_all_satellites
)

from src.mission_schedule import (
    build_combined_schedule,
    print_combined_schedule,
    export_combined_schedule
)


# ============================================================
# SATELLITE CONFIGURATION
# ============================================================

SELECTED_SATELLITE = 1
RUN_ALL_SATELLITES = True

# ============================================================
# SATELLITE CATALOG
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
# SELECT SATELLITE
# ============================================================

satellite = select_satellite(
    catalog,
    SELECTED_SATELLITE
)


# ============================================================
# ORBITAL ANALYSIS
# ============================================================

analysis = analyze_orbit(
    satellite
)
orbit_classification = classify_orbit(
    analysis["altitude_km"],
    analysis["period_minutes"],
    analysis["eccentricity"],
    analysis["inclination_deg"]
)

orbit_validation = (
    validate_orbital_parameters(
        analysis
    )
)

# ============================================================
# BUILD SATELLITE PROFILE
# ============================================================

satellite_profile = build_satellite_profile(
    satellite,
    analysis,
    orbit_classification,
    orbit_validation,
    catalog[
        satellite.name
    ]["tle_file"]
)
# ============================================================
# SATELLITE PROFILE
# ============================================================

print_satellite_profile(
    satellite_profile
)
# ============================================================
# DISPLAY ORBITAL ANALYSIS
# ============================================================

print("=" * 60)

print(
    "                 ORBITAL ANALYSIS"
)

print("=" * 60)


print(
    f"\nSatellite          : "
    f"{satellite.name}"
)


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



if orbit_validation["warnings"]:

    print("\nWarnings:")

    for warning in (
        orbit_validation["warnings"]
    ):

        print(
            f"- {warning}"
        )

if orbit_validation["errors"]:

    print("\nErrors:")

    for error in (
        orbit_validation["errors"]
    ):

        print(
            f"- {error}"
        )


# ============================================================
# DERIVED ORBITAL PARAMETERS
# ============================================================

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


# ============================================================
# PERIGEE / APOGEE
# ============================================================

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


# ============================================================
# ORBITAL VELOCITY
# ============================================================

print("\nORBITAL VELOCITY")

print("-" * 60)


print(
    f"Perigee Velocity   : "
    f"{analysis['perigee_velocity_km_s']:.4f} km/s"
)


print(
    f"Apogee Velocity    : "
    f"{analysis['apogee_velocity_km_s']:.4f} km/s"
)

# ============================================================
# SKYFIELD TIMESCALE
# ============================================================

ts = load.timescale()


# ============================================================
# CURRENT SATELLITE POSITION
# ============================================================

observation_time = ts.now()


latitude, longitude, altitude = satellite_latlon(
    satellite,
    observation_time
)


print("\nCURRENT GROUND POSITION")

print("-" * 60)


print(
    f"Latitude  : "
    f"{latitude:.4f}°"
)


print(
    f"Longitude : "
    f"{longitude:.4f}°"
)


print(
    f"Altitude  : "
    f"{altitude:.2f} km"
)


# ============================================================
# GROUND TRACK CONFIGURATION
# ============================================================

start_time = observation_time

period_minutes = analysis[
    "period_minutes"
]


time_minutes = np.linspace(
    0,
    period_minutes,
    500
)


times = ts.utc(
    start_time.utc_datetime().year,
    start_time.utc_datetime().month,
    start_time.utc_datetime().day,
    start_time.utc_datetime().hour,
    start_time.utc_datetime().minute,
    start_time.utc_datetime().second
    + time_minutes * 60
)


# ============================================================
# GENERATE GROUND TRACK
# ============================================================

latitudes, longitudes, altitudes = (
    generate_ground_track(
        satellite,
        times
    )
)


# ============================================================
# DISPLAY GROUND TRACK SAMPLE
# ============================================================

print("\nGROUND TRACK SAMPLE")

print("-" * 60)


for i in range(
    0,
    500,
    50
):

    print(
        f"Lat: {latitudes[i]:8.3f}°   "
        f"Lon: {longitudes[i]:9.3f}°   "
        f"Alt: {altitudes[i]:8.2f} km"
    )


# ============================================================
# GROUND TRACK PLOTS
# ============================================================

plot_ground_track(
    latitudes,
    longitudes
)


plot_ground_track_map(
    latitudes,
    longitudes
)


# ============================================================
# GROUND STATION CONFIGURATION
# ============================================================

station_name = "Chennai"

station_latitude = 13.0827

station_longitude = 80.2707

station_elevation = 0.0


station = create_ground_station(
    station_latitude,
    station_longitude,
    station_elevation
)


# ============================================================
# CURRENT GROUND STATION OBSERVATION
# ============================================================

observation = observe_satellite(
    satellite,
    observation_time,
    station,
    station_latitude,
    station_longitude
)


print("\nGROUND STATION OBSERVATION")

print("-" * 60)


print(
    f"Ground Station     : "
    f"{station_name}"
)


print(
    f"Range              : "
    f"{observation['range_km']:.2f} km"
)


print(
    f"Azimuth            : "
    f"{observation['azimuth_deg']:.2f}°"
)


print(
    f"Elevation          : "
    f"{observation['elevation_deg']:.2f}°"
)


# ============================================================
# SKYFIELD VALIDATION
# ============================================================

skyfield_observation = validate_with_skyfield(
    satellite,
    observation_time,
    station
)


print("\nVALIDATION")

print("-" * 60)


print(
    f"Our Range       : "
    f"{observation['range_km']:.3f} km"
)


print(
    f"Skyfield Range  : "
    f"{skyfield_observation['range_km']:.3f} km"
)


print()


print(
    f"Our Azimuth     : "
    f"{observation['azimuth_deg']:.3f}°"
)


print(
    f"Skyfield Azimuth: "
    f"{skyfield_observation['azimuth_deg']:.3f}°"
)


print()


print(
    f"Our Elevation   : "
    f"{observation['elevation_deg']:.3f}°"
)


print(
    f"Skyfield Elev.  : "
    f"{skyfield_observation['elevation_deg']:.3f}°"
)


# ============================================================
# PREDICTION CONFIGURATION
# ============================================================

prediction_config = create_prediction_config(
    duration_minutes=720,
    step_seconds=10,
    elevation_mask_deg=10.0
)

print_prediction_config(
    prediction_config
)

prediction_times = generate_prediction_times(
    ts,
    observation_time,
    duration_minutes=(
        prediction_config[
            "duration_minutes"
        ]
    ),
    step_seconds=(
        prediction_config[
            "step_seconds"
        ]
    )
)

# ============================================================
# MULTI-SATELLITE PREDICTION
# ============================================================

if RUN_ALL_SATELLITES:

    print(
        "\n" + "=" * 60
    )

    print(
        "        MULTI-SATELLITE PREDICTION"
    )

    print(
        "=" * 60
    )

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

        # ========================================================
    # BUILD COMBINED MISSION SCHEDULE
    # ========================================================

    combined_schedule = (
        build_combined_schedule(
            all_predictions
        )
    )


    # ========================================================
    # DISPLAY COMBINED MISSION SCHEDULE
    # ========================================================

    print_combined_schedule(
        combined_schedule
    )

        # ========================================================
    # EXPORT COMBINED MISSION SCHEDULE
    # ========================================================

    export_combined_schedule(
        combined_schedule,
        "output/combined_mission_schedule.csv",
        station_name,
        station_latitude,
        station_longitude,
        observation_time,
        prediction_config[
            "duration_minutes"
        ],
        prediction_config[
            "step_seconds"
        ],
        prediction_config[
            "elevation_mask_deg"
        ]
    )

    print(
        "\nCombined mission schedule exported to:"
    )

    print(
        "output/combined_mission_schedule.csv"
    )

if RUN_ALL_SATELLITES:

    print(
        "\n" + "=" * 60
    )

    print(
        "        MULTI-SATELLITE SUMMARY"
    )

    print(
        "=" * 60
    )

    for satellite_name, prediction in (
        all_predictions.items()
    ):

        report = (
            prediction[
                "prediction_report"
            ]
        )

        print(
            f"\nSatellite : "
            f"{satellite_name}"
        )

        print(
            f"Passes    : "
            f"{report['total_passes']}"
        )

        if (
            report["best_pass"]
            is not None
        ):

            print(
                f"Best Max Elevation : "
                f"{report['best_pass'].max_elevation_deg:.2f}°"
            )

        else:

            print(
                "Best Max Elevation : "
                "No visible pass"
            )



# ============================================================
# CALCULATE ELEVATION PROFILE
# ============================================================

elevations = calculate_elevation_profile(
    satellite,
    station,
    prediction_times,
    station_latitude,
    station_longitude
)


# ============================================================
# FIND VISIBILITY INTERVALS
# ============================================================

visibility_intervals = find_visibility_intervals(
    prediction_times,
    elevations,
    elevation_mask_deg=(
        prediction_config[
            "elevation_mask_deg"
        ]
    )
)


# ============================================================
# BUILD STRUCTURED PASS RESULTS
# ============================================================


pass_results = build_pass_results(
    ts,
    satellite,
    station,
    station_latitude,
    station_longitude,
    prediction_times,
    elevations,
    visibility_intervals,
    prediction_config[
        "elevation_mask_deg"
    ]
)
# ============================================================
# BUILD PREDICTION REPORT
# ============================================================

prediction_report = (
    build_prediction_report(
        pass_results
    )
)
# ============================================================
# DISPLAY PREDICTION REPORT
# ============================================================

print_prediction_report(
    prediction_report
)

# ============================================================
# PASS PREDICTION SUMMARY
# ============================================================

print("\nPASS PREDICTION")

print("-" * 60)


print(
    f"Prediction window : "
    f"{prediction_config['duration_minutes']} minutes"
)


print(
    f"Elevation mask    : "
    f"{prediction_config['elevation_mask_deg']:.1f}°"
)


print(
    f"Passes detected   : "
    f"{len(pass_results)}"
)


# ============================================================
# PASS TABLE
# ============================================================

print_pass_summary(
    pass_results
)


# ============================================================
# EXPORT PASS SCHEDULE
# ============================================================

export_passes_to_csv(
    pass_results,
    "output/pass_schedule.csv",
    satellite.name,
    station_name,
    station_latitude,
    station_longitude,
    observation_time,
    prediction_config[
        "duration_minutes"
    ],
    prediction_config[
        "step_seconds"
    ],
    prediction_config[
        "elevation_mask_deg"
    ],
    satellite.epoch
)


# ============================================================
# EXPORT SUMMARY
# ============================================================

print("\n" + "=" * 60)

print(
    "PASS SCHEDULE EXPORT"
)

print("=" * 60)


print(
    f"Satellite        : "
    f"{satellite.name}"
)


print(
    f"Ground Station   : "
    f"{station_name}"
)


print(
    f"Prediction Window: "
    f"{prediction_config['duration_minutes']} minutes"
)


print(
    f"Prediction Window: "
    f"{prediction_config['duration_minutes']} minutes"
)


print(
    f"Passes Detected  : "
    f"{len(pass_results)}"
)


print(
    "CSV File         : "
    "output/pass_schedule.csv"
)


print("=" * 60)


# ============================================================
# ELEVATION PROFILE PLOT
# ============================================================

plot_elevation_profile(
    prediction_times,
    elevations,
    pass_results,
    prediction_config[
        "elevation_mask_deg"
    ]
)