import math

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from skyfield.api import load

from src.satellite_catalog import load_satellite_catalog
from src.pass_prediction import (
    generate_prediction_times,
    calculate_elevation_profile,
    find_visibility_intervals,
    build_pass_results,
)
from src.ground_station import create_ground_station
from src.ground_track import generate_ground_track
from src.orbit_analysis import analyze_orbit


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Satellite Pass Prediction",
    page_icon="🛰️",
    layout="wide",
)


# ============================================================
# GROUND STATIONS
# ============================================================

GROUND_STATIONS = {
    "Chennai": {
        "latitude": 13.0827,
        "longitude": 80.2707,
        "elevation": 0.0,
    },
    "Bengaluru": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "elevation": 0.0,
    },
    "Hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "elevation": 0.0,
    },
    "Mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "elevation": 0.0,
    },
    "Delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "elevation": 0.0,
    },
    "Sriharikota": {
        "latitude": 13.7199,
        "longitude": 80.2304,
        "elevation": 0.0,
    },
}


# ============================================================
# LOAD SATELLITE CATALOG
# ============================================================

satellite_catalog = load_satellite_catalog("data/tle")

satellite_names = list(
    satellite_catalog.keys()
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_results" not in st.session_state:
    st.session_state.prediction_results = []

if "ground_tracks" not in st.session_state:
    st.session_state.ground_tracks = {}

if "last_prediction_config" not in st.session_state:
    st.session_state.last_prediction_config = None

if "prediction_completed" not in st.session_state:
    st.session_state.prediction_completed = False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_pass_value(
    pass_result,
    field_name,
    default=None,
):
    """
    Read a PassResult whether it is an object
    or a dictionary.
    """

    if isinstance(pass_result, dict):
        return pass_result.get(
            field_name,
            default,
        )

    return getattr(
        pass_result,
        field_name,
        default,
    )


def format_time(
    time_value,
    fmt="%Y-%m-%d %H:%M:%S UTC",
):
    """
    Safely format a Skyfield Time object.
    """

    if time_value is None:
        return "N/A"

    if hasattr(
        time_value,
        "utc_strftime",
    ):
        return time_value.utc_strftime(fmt)

    return str(time_value)


def pass_sort_key(pass_result):
    """
    Sort passes using Skyfield's Julian time.
    """

    aos_time = get_pass_value(
        pass_result,
        "aos_time",
    )

    if aos_time is None:
        return float("inf")

    if hasattr(aos_time, "tt"):
        return float(aos_time.tt)

    return float("inf")


def build_pass_dataframe(
    pass_results,
):
    """
    Convert PassResult objects into a
    pandas DataFrame for Streamlit.
    """

    rows = []

    for pass_result in pass_results:

        duration = get_pass_value(
            pass_result,
            "duration_minutes",
        )

        # Backward-compatible fallback
        # if duration_minutes is unavailable.
        if duration is None:

            aos = get_pass_value(
                pass_result,
                "aos_time",
            )

            los = get_pass_value(
                pass_result,
                "los_time",
            )

            if (
                aos is not None
                and los is not None
                and hasattr(aos, "tt")
                and hasattr(los, "tt")
            ):

                duration = (
                    float(los.tt)
                    - float(aos.tt)
                ) * 24.0 * 60.0

        rows.append(
            {
                "Satellite":
                    get_pass_value(
                        pass_result,
                        "satellite_name",
                        "Unknown",
                    ),

                "AOS":
                    format_time(
                        get_pass_value(
                            pass_result,
                            "aos_time",
                        )
                    ),

                "Maximum Elevation":
                    (
                        f"{float(get_pass_value(pass_result, 'max_elevation_deg', 0.0)):.2f}°"
                    ),

                "MAX Time":
                    format_time(
                        get_pass_value(
                            pass_result,
                            "max_elevation_time",
                        )
                    ),

                "LOS":
                    format_time(
                        get_pass_value(
                            pass_result,
                            "los_time",
                        )
                    ),

                "Duration":
                    (
                        f"{float(duration):.2f} min"
                        if duration is not None
                        else "N/A"
                    ),
            }
        )

    return pd.DataFrame(rows)


def create_ground_track_figure(
    latitudes,
    longitudes,
    satellite_name,
):
    """
    Create longitude-vs-latitude ground track.

    Dateline crossings are separated so matplotlib
    does not draw a false vertical line.
    """

    plot_longitudes = []
    plot_latitudes = []

    for index in range(
        len(longitudes)
    ):

        longitude = float(
            longitudes[index]
        )

        latitude = float(
            latitudes[index]
        )

        if index > 0:

            previous_longitude = float(
                longitudes[index - 1]
            )

            if (
                abs(
                    longitude
                    - previous_longitude
                )
                > 180.0
            ):

                plot_longitudes.append(
                    None
                )

                plot_latitudes.append(
                    None
                )

        plot_longitudes.append(
            longitude
        )

        plot_latitudes.append(
            latitude
        )

    figure, axis = plt.subplots(
        figsize=(12, 5)
    )

    axis.plot(
        plot_longitudes,
        plot_latitudes,
        linewidth=1.5,
    )

    axis.set_title(
        f"Ground Track — {satellite_name}"
    )

    axis.set_xlabel(
        "Longitude (degrees)"
    )

    axis.set_ylabel(
        "Latitude (degrees)"
    )

    axis.set_xlim(
        -180,
        180,
    )

    axis.set_ylim(
        -90,
        90,
    )

    axis.set_xticks(
        [
            -180,
            -120,
            -60,
            0,
            60,
            120,
            180,
        ]
    )

    axis.set_yticks(
        [
            -90,
            -60,
            -30,
            0,
            30,
            60,
            90,
        ]
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    axis.axhline(
        0,
        linewidth=0.8,
        alpha=0.5,
    )

    axis.axvline(
        0,
        linewidth=0.8,
        alpha=0.5,
    )

    figure.tight_layout()

    return figure


def get_orbital_display_values(
    satellite,
    analysis,
):
    """
    Skyfield stores TLE inclination and RAAN
    internally in radians.

    Convert them explicitly to degrees here.
    """

    inclination_deg = math.degrees(
        float(satellite.model.inclo)
    )

    raan_deg = math.degrees(
        float(satellite.model.nodeo)
    )

    return {
        "inclination_deg":
            inclination_deg,

        "raan_deg":
            raan_deg,

        "eccentricity":
            analysis[
                "eccentricity"
            ],

        "period_minutes":
            analysis[
                "period_minutes"
            ],

        "semi_major_axis_km":
            analysis[
                "semi_major_axis_km"
            ],

        "altitude_km":
            analysis[
                "altitude_km"
            ],

        "perigee_altitude_km":
            analysis[
                "perigee_altitude_km"
            ],

        "apogee_altitude_km":
            analysis[
                "apogee_altitude_km"
            ],

        "mean_motion_rev_day":
            analysis[
                "mean_motion_rev_day"
            ],

        "perigee_velocity_km_s":
            analysis[
                "perigee_velocity_km_s"
            ],

        "apogee_velocity_km_s":
            analysis[
                "apogee_velocity_km_s"
            ],
    }


# ============================================================
# TITLE
# ============================================================

st.title(
    "🛰️ Satellite Pass Prediction System"
)

st.write(
    "Multi-satellite orbital propagation, "
    "ground-track generation and pass prediction."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "Mission Configuration"
)


# ============================================================
# SATELLITE SELECTION
# ============================================================

selected_satellites = (
    st.sidebar.multiselect(
        "Select Satellites",
        satellite_names,
        default=satellite_names,
    )
)


# ============================================================
# GROUND STATION
# ============================================================

# ============================================================
# GROUND STATION / CUSTOM LOCATION
# ============================================================

st.sidebar.subheader("📍 Observer Location")

location_mode = st.sidebar.radio(
    "Location Mode",
    [
        "Predefined Ground Station",
        "Custom Location",
    ],
)


if location_mode == "Predefined Ground Station":

    station_name = st.sidebar.selectbox(
        "Ground Station",
        list(GROUND_STATIONS.keys()),
    )

    station_data = GROUND_STATIONS[
        station_name
    ]

    station_latitude = station_data[
        "latitude"
    ]

    station_longitude = station_data[
        "longitude"
    ]

    station_elevation = station_data[
        "elevation"
    ]


else:

    custom_location_name = (
        st.sidebar.text_input(
            "Location Name",
            value="Custom Location",
        )
    )

    station_latitude = (
        st.sidebar.number_input(
            "Latitude (°)",
            min_value=-90.0,
            max_value=90.0,
            value=0.0,
            step=0.0001,
            format="%.4f",
        )
    )

    station_longitude = (
        st.sidebar.number_input(
            "Longitude (°)",
            min_value=-180.0,
            max_value=180.0,
            value=0.0,
            step=0.0001,
            format="%.4f",
        )
    )

    station_elevation = (
        st.sidebar.number_input(
            "Elevation (m)",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=1.0,
        )
    )

    station_name = (
        custom_location_name.strip()
    )

    if not station_name:

        station_name = (
            "Custom Location"
        )


# ============================================================
# PREDICTION WINDOW
# ============================================================

prediction_window = (
    st.sidebar.number_input(
        "Prediction Window (minutes)",
        min_value=10,
        max_value=1440,
        value=720,
        step=10,
    )
)


# ============================================================
# ELEVATION MASK
# ============================================================

elevation_mask = (
    st.sidebar.number_input(
        "Elevation Mask (degrees)",
        min_value=0.0,
        max_value=90.0,
        value=10.0,
        step=1.0,
    )
)


# ============================================================
# VALIDATE SATELLITE SELECTION
# ============================================================

if not selected_satellites:

    st.sidebar.warning(
        "Please select at least one satellite."
    )


# ============================================================
# RUN BUTTON
# ============================================================

run_prediction = (
    st.sidebar.button(
        "🚀 Run Prediction",
        disabled=(
            not selected_satellites
        ),
        width="stretch",
    )
)


# ============================================================
# SELECT SATELLITE OBJECTS
# ============================================================

selected_satellite_objects = [

    satellite_catalog[
        satellite_name
    ]["satellite"]

    for satellite_name
    in selected_satellites
]


# ============================================================
# MISSION OVERVIEW
# ============================================================


st.subheader(
    "Mission Overview"
)

col1, col2, col3, col4 = (
    st.columns(4)
)


with col1:

    st.metric(
        "Observer Location",
        station_name,
    )


with col2:

    st.metric(
        "Latitude",
        f"{station_latitude:.4f}°",
    )


with col3:

    st.metric(
        "Longitude",
        f"{station_longitude:.4f}°",
    )


with col4:

    st.metric(
        "Prediction Window",
        f"{prediction_window} min",
    )

# ============================================================
# SELECTED SATELLITES
# ============================================================

st.subheader(
    "Selected Satellites"
)

if selected_satellites:

    st.info(
        "🛰️ "
        + " • ".join(
            selected_satellites
        )
    )

else:

    st.info(
        "No satellites selected."
    )


# ============================================================
# RUN PREDICTION
# ============================================================

if run_prediction:

    # --------------------------------------------------------
    # GROUND STATION
    # --------------------------------------------------------

    # ============================================================
    # CREATE SELECTED OBSERVER STATION
    # ============================================================

    station = create_ground_station(
        station_latitude,
        station_longitude,
        station_elevation,
    )

    # --------------------------------------------------------
    # TIME SCALE
    # --------------------------------------------------------

    ts = load.timescale()

    observation_time = (
        ts.now()
    )

    # --------------------------------------------------------
    # FRESH RESULT CONTAINERS
    # --------------------------------------------------------

    combined_pass_results = []

    combined_ground_tracks = {}

    # --------------------------------------------------------
    # GROUND TRACK TIME GRID
    # --------------------------------------------------------

    ground_track_times = (
        generate_prediction_times(
            ts,
            observation_time,
            duration_minutes=int(
                prediction_window
            ),
            step_seconds=60,
        )
    )

    # --------------------------------------------------------
    # PROGRESS
    # --------------------------------------------------------

    progress_bar = st.progress(
        0.0
    )

    total_satellites = len(
        selected_satellite_objects
    )

    # --------------------------------------------------------
    # PROCESS SATELLITES
    # --------------------------------------------------------

    for index, (
        satellite_name,
        satellite,
    ) in enumerate(
        zip(
            selected_satellites,
            selected_satellite_objects,
        )
    ):

        # ====================================================
        # PASS PREDICTION TIME GRID
        # ====================================================

        prediction_times = (
            generate_prediction_times(
                ts,
                observation_time,
                duration_minutes=int(
                    prediction_window
                ),
                step_seconds=10,
            )
        )

        # ====================================================
        # ELEVATION PROFILE
        # ====================================================

        elevations = (
            calculate_elevation_profile(
                satellite,
                station,
                prediction_times,
                station_latitude,
                station_longitude,
            )
        )

        # ====================================================
        # VISIBILITY INTERVALS
        # ====================================================

        visibility_intervals = (
            find_visibility_intervals(
                prediction_times,
                elevations,
                elevation_mask_deg=(
                    float(elevation_mask)
                ),
            )
        )

        # ====================================================
        # BUILD PASSES
        # ====================================================

        satellite_pass_results = (
            build_pass_results(
                ts,
                satellite,
                station,
                station_latitude,
                station_longitude,
                prediction_times,
                elevations,
                visibility_intervals,
                float(elevation_mask),
            )
        )

        # ====================================================
        # COMBINE ALL SATELLITE PASSES
        # ====================================================

        if satellite_pass_results:

            combined_pass_results.extend(
                list(
                    satellite_pass_results
                )
            )

        # ====================================================
        # GROUND TRACK
        # ====================================================

        latitudes, longitudes, altitudes = (
            generate_ground_track(
                satellite,
                ground_track_times,
            )
        )

        combined_ground_tracks[
            satellite_name
        ] = {
            "latitude":
                latitudes,

            "longitude":
                longitudes,

            "altitude":
                altitudes,
        }

        # ====================================================
        # UPDATE PROGRESS
        # ====================================================

        progress_bar.progress(
            (index + 1)
            / total_satellites
        )

    progress_bar.empty()

    # --------------------------------------------------------
    # SORT ALL PASSES
    # --------------------------------------------------------

    combined_pass_results.sort(
        key=pass_sort_key
    )

    # --------------------------------------------------------
    # SAVE EVERYTHING TO SESSION STATE
    #
    # THIS IS THE IMPORTANT FIX.
    #
    # Streamlit reruns the entire script whenever a widget
    # changes. Therefore prediction results must persist in
    # session_state.
    # --------------------------------------------------------

    st.session_state.prediction_results = (
        list(
            combined_pass_results
        )
    )

    st.session_state.ground_tracks = (
        dict(
            combined_ground_tracks
        )
    )

    st.session_state.last_prediction_config = {

        "satellites":
            list(
                selected_satellites
            ),

        "station":
            station_name,

        "latitude":
            float(
                station_latitude
            ),

        "longitude":
            float(
                station_longitude
            ),

        "elevation":
            float(
                station_elevation
            ),

        "prediction_window":
            int(
                prediction_window
            ),

        "elevation_mask":
            float(
                elevation_mask
            ),

        "observation_time":
            observation_time,
    }

        

    st.session_state.prediction_completed = (
        True
    )

    st.success(
        "✅ Prediction completed successfully."
    )


# ============================================================
# LOAD STORED RESULTS
#
# ALWAYS load these AFTER the prediction block.
# ============================================================

all_pass_results = list(
    st.session_state.prediction_results
)

ground_tracks = dict(
    st.session_state.ground_tracks
)

prediction_completed = (
    st.session_state.prediction_completed
)


# ============================================================
# PREDICTION SUMMARY
# ============================================================

if prediction_completed:

    st.subheader(
        "📊 Prediction Summary"
    )

    summary_col1, summary_col2 = (
        st.columns(2)
    )

    with summary_col1:

        st.metric(
            "Total Passes",
            len(
                all_pass_results
            ),
        )

    with summary_col2:

        last_config = (
            st.session_state
            .last_prediction_config
        )

        satellite_count = (
            len(
                last_config[
                    "satellites"
                ]
            )
            if last_config
            else 0
        )

        st.metric(
            "Satellites",
            satellite_count,
        )


# ============================================================
# NEXT UPCOMING PASS
# ============================================================

st.subheader(
    "⏭️ Next Upcoming Pass"
)

if prediction_completed:

    if all_pass_results:

        next_pass = min(
            all_pass_results,
            key=pass_sort_key,
        )

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            st.metric(
                "Satellite",
                get_pass_value(
                    next_pass,
                    "satellite_name",
                    "Unknown",
                ),
            )

        with col2:

            st.metric(
                "AOS",
                format_time(
                    get_pass_value(
                        next_pass,
                        "aos_time",
                    ),
                    "%H:%M:%S UTC",
                ),
            )

        with col3:

            max_elevation = (
                get_pass_value(
                    next_pass,
                    "max_elevation_deg",
                    0.0,
                )
            )

            st.metric(
                "Maximum Elevation",
                f"{float(max_elevation):.2f}°",
            )

        with col4:

            duration = (
                get_pass_value(
                    next_pass,
                    "duration_minutes",
                )
            )

            st.metric(
                "Duration",
                (
                    f"{float(duration):.2f} min"
                    if duration is not None
                    else "N/A"
                ),
            )

    else:

        st.info(
            "No visible passes were found "
            "for the selected configuration."
        )

else:

    st.info(
        "Run a prediction to see "
        "the next upcoming pass."
    )


# ============================================================
# PASS SCHEDULE
# ============================================================

st.subheader(
    "🛰️ Pass Schedule"
)

if prediction_completed:

    if all_pass_results:

        pass_dataframe = (
            build_pass_dataframe(
                all_pass_results
            )
        )

        st.dataframe(
            pass_dataframe,
            width="stretch",
            hide_index=True,
        )

        # ----------------------------------------------------
        # CSV EXPORT
        # ----------------------------------------------------

        csv_data = (
            pass_dataframe
            .to_csv(
                index=False
            )
            .encode("utf-8")
        )

        st.download_button(
            label=(
                "📥 Download Pass Schedule CSV"
            ),
            data=csv_data,
            file_name=(
                "satellite_pass_schedule.csv"
            ),
            mime="text/csv",
            width="stretch",
        )

    else:

        st.info(
            "No visible passes were found "
            "for the selected configuration."
        )

else:

    st.info(
        "Run a prediction to generate "
        "the pass schedule."
    )


# ============================================================
# ORBITAL PARAMETERS
# ============================================================

st.subheader(
    "🛰️ Orbital Parameters"
)

if selected_satellites:

    orbital_satellite = (
        st.selectbox(
            "Select satellite",
            selected_satellites,
            key=(
                "orbital_parameter_selector"
            ),
        )
    )

    orbital_satellite_object = (
        satellite_catalog[
            orbital_satellite
        ]["satellite"]
    )

    orbital_analysis = (
        analyze_orbit(
            orbital_satellite_object
        )
    )

    orbital_display = (
        get_orbital_display_values(
            orbital_satellite_object,
            orbital_analysis,
        )
    )

    st.write(
        f"### {orbital_satellite}"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Inclination",
            (
                f"{orbital_display['inclination_deg']:.2f}°"
            ),
        )

    with col2:

        st.metric(
            "Eccentricity",
            (
                f"{orbital_display['eccentricity']:.6f}"
            ),
        )

    with col3:

        st.metric(
            "RAAN",
            (
                f"{orbital_display['raan_deg']:.2f}°"
            ),
        )

    with col4:

        st.metric(
            "Orbital Period",
            (
                f"{orbital_display['period_minutes']:.2f} min"
            ),
        )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Semi-Major Axis",
            (
                f"{orbital_display['semi_major_axis_km']:.2f} km"
            ),
        )

    with col2:

        st.metric(
            "Altitude",
            (
                f"{orbital_display['altitude_km']:.2f} km"
            ),
        )

    with col3:

        st.metric(
            "Perigee Altitude",
            (
                f"{orbital_display['perigee_altitude_km']:.2f} km"
            ),
        )

    with col4:

        st.metric(
            "Apogee Altitude",
            (
                f"{orbital_display['apogee_altitude_km']:.2f} km"
            ),
        )

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        st.metric(
            "Mean Motion",
            (
                f"{orbital_display['mean_motion_rev_day']:.4f} rev/day"
            ),
        )

    with col2:

        st.metric(
            "Perigee Velocity",
            (
                f"{orbital_display['perigee_velocity_km_s']:.4f} km/s"
            ),
        )

    with col3:

        st.metric(
            "Apogee Velocity",
            (
                f"{orbital_display['apogee_velocity_km_s']:.4f} km/s"
            ),
        )

else:

    st.info(
        "Select a satellite to view "
        "orbital parameters."
    )


# ============================================================
# GROUND TRACK
# ============================================================

st.subheader(
    "🌍 Ground Track"
)

if ground_tracks:

    ground_track_satellite = (
        st.selectbox(
            "Select satellite for ground track",
            list(
                ground_tracks.keys()
            ),
            key="ground_track_selector",
        )
    )

    track_data = (
        ground_tracks.get(
            ground_track_satellite
        )
    )

    if track_data is not None:

        ground_track_figure = (
            create_ground_track_figure(
                track_data[
                    "latitude"
                ],
                track_data[
                    "longitude"
                ],
                ground_track_satellite,
            )
        )

        st.pyplot(
            ground_track_figure,
            width="stretch",
        )

        plt.close(
            ground_track_figure
        )

        altitude_values = (
            track_data[
                "altitude"
            ]
        )

        if len(
            altitude_values
        ) > 0:

            ground_track_col1, ground_track_col2 = (
                st.columns(2)
            )

            with ground_track_col1:

                st.metric(
                    "Minimum Altitude",
                    (
                        f"{min(altitude_values):.2f} km"
                    ),
                )

            with ground_track_col2:

                st.metric(
                    "Maximum Altitude",
                    (
                        f"{max(altitude_values):.2f} km"
                    ),
                )

else:

    st.info(
        "Run a prediction to generate "
        "the ground track."
    )


# ============================================================
# LAST RUN INFORMATION
# ============================================================

if (
    st.session_state
    .last_prediction_config
    is not None
):

    st.divider()

    st.caption(
        "Last prediction configuration"
    )

    last_config = (
        st.session_state
        .last_prediction_config
    )

    st.write(
        f"**Satellites:** "
        f"{', '.join(last_config['satellites'])}"
    )

    st.write(
        f"**Observer Location:** "
        f"{last_config['station']}"
    )

    st.write(
        f"**Coordinates:** "
        f"{last_config['latitude']:.4f}°, "
        f"{last_config['longitude']:.4f}°"
    )

    st.write(
        f"**Prediction Window:** "
        f"{last_config['prediction_window']} minutes"
    )

    st.write(
        f"**Elevation Mask:** "
        f"{last_config['elevation_mask']:.1f}°"
    )