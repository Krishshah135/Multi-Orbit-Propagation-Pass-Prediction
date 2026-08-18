import numpy as np
from dataclasses import dataclass

@dataclass
class PassResult:
    """
    Stores all important information
    about one satellite pass.
    """

    satellite_name: str

    aos_time: object
    los_time: object

    max_elevation_deg: float
    max_elevation_time: object

    duration_minutes: float

    elevation_mask_deg: float

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

def refine_crossing_time(
    ts,
    time_before,
    time_after,
    elevation_before,
    elevation_after,
    elevation_mask_deg=0.0
):
    """
    Refine the time at which the satellite
    crosses the elevation mask.

    Uses linear interpolation between two
    surrounding elevation samples.

    Returns:
        Skyfield Time object representing
        the estimated crossing time.
    """

    denominator = (
        elevation_after
        - elevation_before
    )

    # Prevent division by zero
    if denominator == 0:
        return time_before

    fraction = (
        elevation_mask_deg
        - elevation_before
    ) / denominator

    # Keep interpolation inside the interval
    fraction = np.clip(
        fraction,
        0.0,
        1.0
    )

    crossing_tt = (
        time_before.tt
        + fraction
        * (
            time_after.tt
            - time_before.tt
        )
    )

    return ts.tt_jd(crossing_tt)

def refine_pass_times(
    ts,
    times,
    elevations,
    start_index,
    end_index,
    elevation_mask_deg=0.0
):
    """
    Refine AOS and LOS times for one
    visibility interval.

    Returns:
        aos_time
        los_time
    """

    # --------------------------------------------------
    # AOS
    # --------------------------------------------------

    if start_index == 0:

        aos_time = times[0]

    else:

        aos_time = refine_crossing_time(
            ts,
            times[start_index - 1],
            times[start_index],
            elevations[start_index - 1],
            elevations[start_index],
            elevation_mask_deg
        )


    # --------------------------------------------------
    # LOS
    # --------------------------------------------------

    if end_index == len(times) - 1:

        los_time = times[-1]

    else:

        los_time = refine_crossing_time(
            ts,
            times[end_index],
            times[end_index + 1],
            elevations[end_index],
            elevations[end_index + 1],
            elevation_mask_deg
        )


    return (
        aos_time,
        los_time
    )

def refine_max_elevation(
    ts,
    satellite,
    station,
    latitude_deg,
    longitude_deg,
    times,
    elevations,
    start_index,
    end_index
):
    """
    Refine the maximum elevation of a satellite pass.

    The initial maximum is found from the sampled
    elevation profile. A quadratic interpolation
    around that maximum is then used to estimate
    the true peak time.

    Returns:
        refined_max_elevation_deg
        refined_max_time
    """

    from src.ground_station import (
        observe_satellite
    )

    # --------------------------------------------------
    # 1. Find the sampled maximum
    # --------------------------------------------------

    pass_elevations = elevations[
        start_index:end_index + 1
    ]

    local_max_index = np.argmax(
        pass_elevations
    )

    max_index = (
        start_index
        + local_max_index
    )


    # --------------------------------------------------
    # 2. Check whether the maximum is at
    #    the edge of the prediction interval
    # --------------------------------------------------

    if (
        max_index == start_index
        or max_index == end_index
        or max_index == 0
        or max_index == len(elevations) - 1
    ):

        max_time = times[max_index]

        observation = observe_satellite(
            satellite,
            max_time,
            station,
            latitude_deg,
            longitude_deg
        )

        return (
            observation["elevation_deg"],
            max_time
        )


    # --------------------------------------------------
    # 3. Get the three points around the maximum
    # --------------------------------------------------

    previous_index = max_index - 1
    next_index = max_index + 1

    y1 = elevations[previous_index]
    y2 = elevations[max_index]
    y3 = elevations[next_index]


    # --------------------------------------------------
    # 4. Calculate the sampling interval
    # --------------------------------------------------

    t1 = times[previous_index]
    t2 = times[max_index]
    t3 = times[next_index]

    step_seconds = (
        t3.tt - t2.tt
    ) * 86400.0


    # --------------------------------------------------
    # 5. Quadratic interpolation
    #
    #        y
    #        ▲
    #        │       ●
    #        │     /   \
    #        │   ●       ●
    #        └────────────────→ time
    # --------------------------------------------------

    denominator = (
        y1
        - 2.0 * y2
        + y3
    )


    # Prevent division by zero
    if abs(denominator) < 1e-12:

        max_time = t2

        observation = observe_satellite(
            satellite,
            max_time,
            station,
            latitude_deg,
            longitude_deg
        )

        return (
            observation["elevation_deg"],
            max_time
        )


    offset_seconds = (
        0.5
        * step_seconds
        * (y1 - y3)
        / denominator
    )


    # Keep the refined point between
    # the surrounding samples

    offset_seconds = np.clip(
        offset_seconds,
        -step_seconds,
        step_seconds
    )


    # --------------------------------------------------
    # 6. Convert refined offset into Skyfield time
    # --------------------------------------------------

    refined_tt = (
        t2.tt
        + offset_seconds / 86400.0
    )

    refined_time = ts.tt_jd(
        refined_tt
    )


    # --------------------------------------------------
    # 7. Calculate actual elevation at
    #    the refined time
    # --------------------------------------------------

    observation = observe_satellite(
        satellite,
        refined_time,
        station,
        latitude_deg,
        longitude_deg
    )

    refined_elevation = (
        observation["elevation_deg"]
    )


    return (
        refined_elevation,
        refined_time
    )

def build_pass_results(
    ts,
    satellite,
    station,
    latitude_deg,
    longitude_deg,
    times,
    elevations,
    visibility_intervals,
    elevation_mask_deg
):
    """
    Convert detected visibility intervals
    into structured PassResult objects.
    """

    pass_results = []

    for start_index, end_index in visibility_intervals:

        # ----------------------------------------------
        # Refine AOS and LOS
        # ----------------------------------------------

        aos_time, los_time = refine_pass_times(
            ts,
            times,
            elevations,
            start_index,
            end_index,
            elevation_mask_deg
        )

        # ----------------------------------------------
        # Refine maximum elevation
        # ----------------------------------------------

        max_elevation, max_elevation_time = (
            refine_max_elevation(
                ts,
                satellite,
                station,
                latitude_deg,
                longitude_deg,
                times,
                elevations,
                start_index,
                end_index
            )
        )

        # ----------------------------------------------
        # Calculate actual duration
        # ----------------------------------------------

        duration_seconds = (
            los_time.tt
            - aos_time.tt
        ) * 86400.0

        duration_minutes = (
            duration_seconds / 60.0
        )

        # ----------------------------------------------
        # Create PassResult
        # ----------------------------------------------

        result = PassResult(
            satellite_name=satellite.name,
            aos_time=aos_time,
            los_time=los_time,
            max_elevation_deg=max_elevation,
            max_elevation_time=max_elevation_time,
            duration_minutes=duration_minutes,
            elevation_mask_deg=elevation_mask_deg
        )

        pass_results.append(result)

    return pass_results

def print_pass_summary(pass_results):
    """
    Print a clean summary table
    of predicted satellite passes.
    """

    print("\nPASS SUMMARY")
    print("=" * 120)

    print(
        f"{'PASS':<6}"
        f"{'AOS':<22}"
        f"{'MAX EL':<12}"
        f"{'MAX TIME':<22}"
        f"{'LOS':<22}"
        f"{'DURATION':<12}"
    )

    print("-" * 120)

    for index, result in enumerate(
        pass_results,
        start=1
    ):

        aos = result.aos_time.utc_strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        max_time = (
            result.max_elevation_time.utc_strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        los = result.los_time.utc_strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print(
            f"{index:<6}"
            f"{aos:<22}"
            f"{result.max_elevation_deg:<12.2f}"
            f"{max_time:<22}"
            f"{los:<22}"
            f"{result.duration_minutes:<12.2f}"
        )

    print("=" * 120)

def plot_elevation_profile(
    times,
    elevations,
    pass_results,
    elevation_mask_deg=0.0
):
    """
    Plot satellite elevation versus time
    and mark AOS, maximum elevation,
    and LOS for each predicted pass.
    """

    import matplotlib.pyplot as plt

    datetime_values = [
        time.utc_datetime()
        for time in times
    ]

    plt.figure(figsize=(14, 6))

    # --------------------------------------------------
    # Elevation profile
    # --------------------------------------------------

    plt.plot(
        datetime_values,
        elevations,
        label="Satellite Elevation"
    )

    # --------------------------------------------------
    # Elevation mask
    # --------------------------------------------------

    plt.axhline(
        elevation_mask_deg,
        linestyle="--",
        label=(
            f"Elevation Mask "
            f"({elevation_mask_deg:.1f}°)"
        )
    )

    # --------------------------------------------------
    # Mark AOS, MAX and LOS
    # --------------------------------------------------

    for index, result in enumerate(
        pass_results,
        start=1
    ):

        aos_datetime = (
            result.aos_time.utc_datetime()
        )

        max_datetime = (
            result.max_elevation_time.utc_datetime()
        )

        los_datetime = (
            result.los_time.utc_datetime()
        )

        # AOS

        plt.scatter(
            aos_datetime,
            elevation_mask_deg,
            marker="o",
            s=60,
            label=f"Pass {index} AOS"
        )

        # Maximum elevation

        plt.scatter(
            max_datetime,
            result.max_elevation_deg,
            marker="^",
            s=80,
            label=f"Pass {index} MAX"
        )

        # LOS

        plt.scatter(
            los_datetime,
            elevation_mask_deg,
            marker="s",
            s=60,
            label=f"Pass {index} LOS"
        )

    # --------------------------------------------------
    # Plot labels
    # --------------------------------------------------

    plt.xlabel(
        "Time (UTC)"
    )

    plt.ylabel(
        "Elevation (degrees)"
    )

    plt.title(
        "ISS Elevation Profile and Pass Events"
    )

    plt.grid(
        True,
        alpha=0.3
    )

    plt.legend()

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    plt.show()



def export_passes_to_csv(
    pass_results,
    filename,
    satellite_name,
    station_name,
    station_latitude,
    station_longitude,
    observation_time,
    prediction_window_minutes,
    prediction_step_seconds,
    elevation_mask_deg,
    satellite_epoch
):
    """
    Export predicted satellite passes
    and prediction metadata to a CSV file.
    """

    import csv
    import os

    # --------------------------------------------------
    # Make sure the output directory exists
    # --------------------------------------------------

    output_directory = os.path.dirname(filename)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # --------------------------------------------------
    # Open CSV file
    # --------------------------------------------------

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)
        writer.writerow(
            [
                "Prediction Step (seconds)",
                    prediction_step_seconds
            ]
        )

        writer.writerow(
            [
                "Elevation Mask (deg)",
                elevation_mask_deg
            ]
        )
        # --------------------------------------------------
        # CSV header
        # --------------------------------------------------

        writer.writerow([
            "Satellite",
            "Ground Station",
            "Station Latitude (deg)",
            "Station Longitude (deg)",
            "Prediction Start (UTC)",
            "Prediction Window (min)",
            "TLE Epoch (UTC)",
            "AOS (UTC)",
            "Maximum Elevation (deg)",
            "Maximum Elevation Time (UTC)",
            "LOS (UTC)",
            "Duration (min)",
            "Elevation Mask (deg)"
        ])

        # --------------------------------------------------
        # Write pass data
        # --------------------------------------------------

        for result in pass_results:

            aos = result.aos_time.utc_strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            max_time = (
                result.max_elevation_time.utc_strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            los = result.los_time.utc_strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            prediction_start = (
                prediction_start_time.utc_strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            tle_epoch_string = (
                tle_epoch.utc_strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            writer.writerow([
                satellite_name,
                station_name,
                f"{station_latitude_deg:.6f}",
                f"{station_longitude_deg:.6f}",
                prediction_start,
                prediction_window_minutes,
                tle_epoch_string,
                aos,
                f"{result.max_elevation_deg:.2f}",
                max_time,
                los,
                f"{result.duration_minutes:.2f}",
                f"{result.elevation_mask_deg:.2f}"
            ])

    print(
        "\nPass schedule exported to:"
    )

    print(
        filename
    )