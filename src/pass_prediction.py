import numpy as np


def calculate_elevation_profile(
    satellite,
    station,
    times,
    latitude_deg,
    longitude_deg
):
    """
    Calculate satellite elevation at
    multiple points in time.

    Returns:
        numpy array of elevation angles
        in degrees.
    """

    from src.ground_station import (
        observe_satellite
    )

    elevations = []

    for time in times:

        observation = observe_satellite(
            satellite,
            time,
            station,
            latitude_deg,
            longitude_deg
        )

        elevations.append(
            observation["elevation_deg"]
        )

    return np.array(elevations)
def generate_prediction_times(
    ts,
    start_time,
    duration_minutes=180,
    step_seconds=10
):
    """
    Generate time samples for pass prediction.

    Parameters:
        ts:
            Skyfield timescale.

        start_time:
            Starting Skyfield time.

        duration_minutes:
            Prediction window.

        step_seconds:
            Time resolution.

    Returns:
        Skyfield Time object.
    """

    total_seconds = (
        duration_minutes * 60
    )

    time_seconds = np.arange(
        0,
        total_seconds + step_seconds,
        step_seconds
    )

    times = ts.utc(
        start_time.utc_datetime().year,
        start_time.utc_datetime().month,
        start_time.utc_datetime().day,
        start_time.utc_datetime().hour,
        start_time.utc_datetime().minute,
        start_time.utc_datetime().second
        + time_seconds
    )

    return times
def find_visibility_intervals(
    times,
    elevations,
    elevation_mask_deg=0.0
):
    """
    Find intervals where the satellite
    is above the elevation mask.

    Returns:
        List of visibility intervals.
    """

    visible = (
        elevations >= elevation_mask_deg
    )

    intervals = []

    start_index = None

    for i in range(len(visible)):

        # Satellite becomes visible
        if visible[i] and start_index is None:

            start_index = i

        # Satellite becomes invisible
        elif (
            not visible[i]
            and start_index is not None
        ):

            end_index = i - 1

            intervals.append(
                (
                    start_index,
                    end_index
                )
            )

            start_index = None

    # Handle a pass that continues
    # until the end of the prediction window

    if start_index is not None:

        intervals.append(
            (
                start_index,
                len(visible) - 1
            )
        )

    return intervals
def find_max_elevation(
    elevations
):
    """
    Find the maximum elevation
    and its array index.

    Returns:
        max_elevation_deg,
        max_index
    """

    max_index = np.argmax(
        elevations
    )

    max_elevation = (
        elevations[max_index]
    )

    return (
        max_elevation,
        max_index
    )