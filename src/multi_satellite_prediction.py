# ============================================================
# MULTI-SATELLITE PREDICTION ENGINE
# ============================================================

from src.pass_prediction import (
    generate_prediction_times,
    calculate_elevation_profile,
    find_visibility_intervals,
    build_pass_results
)

from src.prediction_report import (
    build_prediction_report
)


def predict_satellite_passes(
    ts,
    satellite,
    station,
    station_latitude,
    station_longitude,
    observation_time,
    prediction_config
):
    """
    Generate pass predictions for one satellite.

    This function wraps the existing pass-prediction
    engine so that multiple satellites can use the
    same prediction workflow.
    """

    # --------------------------------------------------------
    # Generate prediction times
    # --------------------------------------------------------

    prediction_times = (
        generate_prediction_times(
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
    )

    # --------------------------------------------------------
    # Calculate elevation profile
    # --------------------------------------------------------

    elevations = (
        calculate_elevation_profile(
            satellite,
            station,
            prediction_times,
            station_latitude,
            station_longitude
        )
    )

    # --------------------------------------------------------
    # Find visible intervals
    # --------------------------------------------------------

    visibility_intervals = (
        find_visibility_intervals(
            prediction_times,
            elevations,
            elevation_mask_deg=(
                prediction_config[
                    "elevation_mask_deg"
                ]
            )
        )
    )

    # --------------------------------------------------------
    # Build structured pass results
    # --------------------------------------------------------

    pass_results = (
        build_pass_results(
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
    )

    # --------------------------------------------------------
    # Build prediction report
    # --------------------------------------------------------

    prediction_report = (
        build_prediction_report(
            pass_results
        )
    )

    # --------------------------------------------------------
    # Return everything needed by the caller
    # --------------------------------------------------------

    return {
        "satellite": satellite,

        "prediction_times":
            prediction_times,

        "elevations":
            elevations,

        "visibility_intervals":
            visibility_intervals,

        "pass_results":
            pass_results,

        "prediction_report":
            prediction_report
    }


def predict_all_satellites(
    ts,
    catalog,
    station,
    station_latitude,
    station_longitude,
    observation_time,
    prediction_config
):
    """
    Run the prediction engine for every satellite
    in the satellite catalog.
    """

    all_predictions = {}

    for satellite_name, satellite_data in (
        catalog.items()
    ):

        satellite = (
            satellite_data["satellite"]
        )

        print(
            "\n" + "=" * 60
        )

        print(
            f"PREDICTING: "
            f"{satellite.name}"
        )

        print(
            "=" * 60
        )

        prediction = (
            predict_satellite_passes(
                ts,
                satellite,
                station,
                station_latitude,
                station_longitude,
                observation_time,
                prediction_config
            )
        )

        all_predictions[
            satellite_name
        ] = prediction

        print(
            f"Passes detected : "
            f"{len(prediction['pass_results'])}"
        )

    return all_predictions