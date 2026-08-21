import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from skyfield.api import load

from src.satellite_catalog import (
    load_satellite_catalog
)

from src.pass_prediction import (
    generate_prediction_times,
    calculate_elevation_profile,
    find_visibility_intervals,
    build_pass_results
)

from src.ground_station import (
    create_ground_station
)

from src.ground_track import (
    generate_ground_track
)
from src.orbit_analysis import analyze_orbit

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Satellite Pass Prediction",
    page_icon="🛰️",
    layout="wide"
)


# ============================================================
# GROUND STATIONS
# ============================================================

GROUND_STATIONS = {

    "Chennai": {
        "latitude": 13.0827,
        "longitude": 80.2707,
        "elevation": 0.0
    },

    "Bengaluru": {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "elevation": 0.0
    },

    "Hyderabad": {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "elevation": 0.0
    },

    "Mumbai": {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "elevation": 0.0
    },

    "Delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090,
        "elevation": 0.0
    },

    "Sriharikota": {
        "latitude": 13.7199,
        "longitude": 80.2304,
        "elevation": 0.0
    }
}


# ============================================================
# LOAD SATELLITE CATALOG
# ============================================================

satellite_catalog = load_satellite_catalog(
    "data/tle"
)

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

selected_satellites = st.sidebar.multiselect(
    "Select Satellites",
    satellite_names,
    default=satellite_names
)


# ============================================================
# GROUND STATION
# ============================================================

station_name = st.sidebar.selectbox(
    "Ground Station",
    list(GROUND_STATIONS.keys())
)


# ============================================================
# PREDICTION WINDOW
# ============================================================

prediction_window = st.sidebar.number_input(
    "Prediction Window (minutes)",
    min_value=10,
    max_value=1440,
    value=720,
    step=10
)


# ============================================================
# ELEVATION MASK
# ============================================================

elevation_mask = st.sidebar.number_input(
    "Elevation Mask (degrees)",
    min_value=0.0,
    max_value=90.0,
    value=10.0,
    step=1.0
)


# ============================================================
# SATELLITE VALIDATION
# ============================================================

if not selected_satellites:

    st.sidebar.warning(
        "Please select at least one satellite."
    )


# ============================================================
# RUN BUTTON
# ============================================================

run_prediction = st.sidebar.button(
    "🚀 Run Prediction",
    disabled=not selected_satellites,
    width="stretch"
)


# ============================================================
# SELECTED SATELLITE OBJECTS
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


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Ground Station",
        station_name
    )


with col2:

    st.metric(
        "Prediction Window",
        f"{prediction_window} min"
    )


with col3:

    st.metric(
        "Elevation Mask",
        f"{elevation_mask:.1f}°"
    )


# ============================================================
# SELECTED SATELLITES
# ============================================================

st.subheader(
    "Selected Satellites"
)


if selected_satellites:

    satellite_text = " • ".join(
        selected_satellites
    )

    st.info(
        f"🛰️ {satellite_text}"
    )

else:

    st.info(
        "No satellites selected."
    )


# ============================================================
# RUN REAL PREDICTION
# ============================================================

if run_prediction:

    # --------------------------------------------------------
    # Ground station information
    # --------------------------------------------------------

    station_data = GROUND_STATIONS[
        station_name
    ]

    station_latitude = (
        station_data["latitude"]
    )

    station_longitude = (
        station_data["longitude"]
    )

    station_elevation = (
        station_data["elevation"]
    )


    # --------------------------------------------------------
    # Create ground station
    # --------------------------------------------------------

    station = create_ground_station(
        station_latitude,
        station_longitude,
        station_elevation
    )


    # --------------------------------------------------------
    # Skyfield time scale
    # --------------------------------------------------------

    ts = load.timescale()

    observation_time = ts.now()


    # --------------------------------------------------------
    # Containers for results
    # --------------------------------------------------------

    all_pass_results = []

    ground_tracks = {}


    # --------------------------------------------------------
    # Ground-track time grid
    # --------------------------------------------------------

    ground_track_times = (
        generate_prediction_times(
            ts,
            observation_time,
            duration_minutes=prediction_window,
            step_seconds=60
        )
    )


    # --------------------------------------------------------
    # Progress bar
    # --------------------------------------------------------

    progress_bar = st.progress(
        0
    )


    # --------------------------------------------------------
    # Process each satellite
    # --------------------------------------------------------

    for index, (
        satellite_name,
        satellite
    ) in enumerate(
        zip(
            selected_satellites,
            selected_satellite_objects
        )
    ):

        # ====================================================
        # PASS PREDICTION TIME GRID
        # ====================================================

        prediction_times = (
            generate_prediction_times(
                ts,
                observation_time,
                duration_minutes=prediction_window,
                step_seconds=10
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
                station_longitude
            )
        )


        # ====================================================
        # VISIBILITY INTERVALS
        # ====================================================

        visibility_intervals = (
            find_visibility_intervals(
                prediction_times,
                elevations,
                elevation_mask_deg=elevation_mask
            )
        )


        # ====================================================
        # BUILD PASS RESULTS
        # ====================================================

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
                elevation_mask
            )
        )


        # ====================================================
        # ADD TO COMBINED RESULTS
        # ====================================================

        all_pass_results.extend(
            pass_results
        )


        # ====================================================
        # GENERATE GROUND TRACK
        # ====================================================

        latitudes, longitudes, altitudes = (
            generate_ground_track(
                satellite,
                ground_track_times
            )
        )


        ground_tracks[
            satellite_name
        ] = {

            "latitude": latitudes,

            "longitude": longitudes,

            "altitude": altitudes
        }


        # ====================================================
        # UPDATE PROGRESS
        # ====================================================

        progress_bar.progress(
            (index + 1)
            / len(selected_satellite_objects)
        )


    # --------------------------------------------------------
    # Finish progress
    # --------------------------------------------------------

    progress_bar.empty()


    # ========================================================
    # SORT PASSES BY AOS
    # ========================================================

    all_pass_results.sort(
        key=lambda result:
            result.aos_time.tt
    )


    # ========================================================
    # SAVE RESULTS TO SESSION STATE
    # ========================================================

    st.session_state.prediction_results = (
        all_pass_results
    )

    st.session_state.ground_tracks = (
        ground_tracks
    )

    st.session_state.last_prediction_config = {

        "satellites":
            list(selected_satellites),

        "station":
            station_name,

        "prediction_window":
            prediction_window,

        "elevation_mask":
            elevation_mask,

        "observation_time":
            observation_time
    }


    # ========================================================
    # SUCCESS MESSAGE
    # ========================================================

    st.success(
        "✅ Prediction completed successfully."
    )


# ============================================================
# LOAD STORED RESULTS
# ============================================================

all_pass_results = (
    st.session_state.prediction_results
)

ground_tracks = (
    st.session_state.ground_tracks
)


# ============================================================
# RESULTS SUMMARY
# ============================================================

if all_pass_results:

    st.subheader(
        "📊 Prediction Summary"
    )


    summary_col1, summary_col2 = (
        st.columns(2)
    )


    with summary_col1:

        st.metric(
            "Total Passes",
            len(all_pass_results)
        )


    with summary_col2:

        st.metric(
            "Satellites",
            len(
                st.session_state
                .last_prediction_config[
                    "satellites"
                ]
            )
        )


# ============================================================
# NEXT UPCOMING PASS
# ============================================================

st.subheader(
    "⏭️ Next Upcoming Pass"
)


if all_pass_results:

    next_pass = min(
        all_pass_results,
        key=lambda result:
            result.aos_time.tt
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


    with col1:

        st.metric(
            "Satellite",
            next_pass.satellite_name
        )


    with col2:

        st.metric(
            "AOS",
            next_pass.aos_time.utc_strftime(
                "%H:%M:%S UTC"
            )
        )


    with col3:

        st.metric(
            "Maximum Elevation",
            f"{next_pass.max_elevation_deg:.2f}°"
        )


    with col4:

        st.metric(
            "Duration",
            f"{next_pass.duration_minutes:.2f} min"
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


if all_pass_results:

    pass_table = []


    for pass_result in all_pass_results:

        pass_table.append(
            {

                "Satellite":
                    pass_result.satellite_name,

                "AOS":
                    pass_result.aos_time.utc_strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                "Maximum Elevation":
                    (
                        f"{pass_result.max_elevation_deg:.2f}°"
                    ),

                "MAX Time":
                    (
                        pass_result
                        .max_elevation_time
                        .utc_strftime(
                            "%Y-%m-%d %H:%M:%S UTC"
                        )
                    ),

                "LOS":
                    pass_result.los_time.utc_strftime(
                        "%Y-%m-%d %H:%M:%S UTC"
                    ),

                "Duration":
                    (
                        f"{pass_result.duration_minutes:.2f} min"
                    )
            }
        )


    pass_dataframe = pd.DataFrame(
        pass_table
    )


    st.dataframe(
        pass_dataframe,
        width="stretch",
        hide_index=True
    )
    # ============================================================
    # CSV EXPORT
    # ============================================================

    csv_data = pass_dataframe.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download Pass Schedule CSV",
        data=csv_data,
        file_name="satellite_pass_schedule.csv",
        mime="text/csv",
        width="stretch"
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

    orbital_satellite = st.selectbox(
        "Select satellite",
        selected_satellites,
        key="orbital_parameter_selector"
    )

    orbital_satellite_object = (
        satellite_catalog[
            orbital_satellite
        ]["satellite"]
    )

    orbital_analysis = analyze_orbit(
        orbital_satellite_object
    )

    st.write(
        f"### {orbital_satellite}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Inclination",
            f"{orbital_analysis['inclination_deg']:.2f}°"
        )

    with col2:

        st.metric(
            "Eccentricity",
            f"{orbital_analysis['eccentricity']:.6f}"
        )

    with col3:

        st.metric(
            "RAAN",
            f"{orbital_analysis['raan_deg']:.2f}°"
        )

    with col4:

        st.metric(
            "Orbital Period",
            f"{orbital_analysis['period_minutes']:.2f} min"
        )


    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Semi-Major Axis",
            f"{orbital_analysis['semi_major_axis_km']:.2f} km"
        )

    with col2:

        st.metric(
            "Altitude",
            f"{orbital_analysis['altitude_km']:.2f} km"
        )

    with col3:

        st.metric(
            "Perigee Altitude",
            f"{orbital_analysis['perigee_altitude_km']:.2f} km"
        )

    with col4:

        st.metric(
            "Apogee Altitude",
            f"{orbital_analysis['apogee_altitude_km']:.2f} km"
        )


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Mean Motion",
            f"{orbital_analysis['mean_motion_rev_day']:.4f} rev/day"
        )

    with col2:

        st.metric(
            "Perigee Velocity",
            f"{orbital_analysis['perigee_velocity_km_s']:.4f} km/s"
        )

    with col3:

        st.metric(
            "Apogee Velocity",
            f"{orbital_analysis['apogee_velocity_km_s']:.4f} km/s"
        )

else:

    st.info(
        "Select a satellite to view orbital parameters."
    )

# ============================================================
# GROUND TRACK FUNCTION
# ============================================================

def create_ground_track_figure(
    latitudes,
    longitudes,
    satellite_name
):
    """
    Create a clean ground-track figure.

    Longitude jumps greater than 180 degrees
    are treated as crossings of the ±180°
    dateline so that matplotlib does not draw
    an artificial vertical line across the map.
    """

    plot_longitudes = []
    plot_latitudes = []


    for index in range(
        len(longitudes)
    ):

        longitude = (
            float(longitudes[index])
        )

        latitude = (
            float(latitudes[index])
        )


        if index > 0:

            previous_longitude = (
                float(longitudes[index - 1])
            )


            if (
                abs(
                    longitude
                    - previous_longitude
                )
                > 180
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
        linewidth=1.5
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
        180
    )


    axis.set_ylim(
        -90,
        90
    )


    axis.set_xticks(
        [
            -180,
            -120,
            -60,
            0,
            60,
            120,
            180
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
            90
        ]
    )


    axis.grid(
        True,
        alpha=0.3
    )


    axis.axhline(
        0,
        linewidth=0.8,
        alpha=0.5
    )


    axis.axvline(
        0,
        linewidth=0.8,
        alpha=0.5
    )


    figure.tight_layout()


    return figure


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
            key="ground_track_selector"
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
                track_data["latitude"],
                track_data["longitude"],
                ground_track_satellite
            )
        )


        st.pyplot(
            ground_track_figure,
            width="stretch"
        )


        plt.close(
            ground_track_figure
        )


        # ----------------------------------------------------
        # Ground-track altitude information
        # ----------------------------------------------------

        altitude_values = (
            track_data["altitude"]
        )


        if len(altitude_values) > 0:

            ground_track_col1, ground_track_col2 = (
                st.columns(2)
            )


            with ground_track_col1:

                st.metric(
                    "Minimum Altitude",
                    (
                        f"{min(altitude_values):.2f} km"
                    )
                )


            with ground_track_col2:

                st.metric(
                    "Maximum Altitude",
                    (
                        f"{max(altitude_values):.2f} km"
                    )
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
    st.session_state.last_prediction_config
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
        f"**Ground Station:** "
        f"{last_config['station']}"
    )


    st.write(
        f"**Prediction Window:** "
        f"{last_config['prediction_window']} minutes"
    )


    st.write(
        f"**Elevation Mask:** "
        f"{last_config['elevation_mask']:.1f}°"
    )