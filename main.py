import numpy as np
from src.tle_loader import load_satellite_from_file
from src.orbit_analysis import analyze_orbit
from skyfield.api import load
from src.visualization import plot_ground_track , plot_ground_track_map
from src.ground_track import satellite_latlon , generate_ground_track
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
    refine_max_elevation
)
# Load satellite data from CelesTrak
satellites = load_satellite_from_file(
    "data/tle/iss.txt"
)


iss = satellites[0]

# Perform orbital analysis
analysis = analyze_orbit(iss)


# Display results
print("=" * 60)
print("                 ORBITAL ANALYSIS")
print("=" * 60)

print(f"\nSatellite          : {iss.name}")

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


print("\nORBITAL VELOCITY")
print("-" * 60)

print(
    f"Perigee Velocity   : "
    f"{analysis['perigee_velocity_km_s']:.4f} km/s"
)

print(
    f"Apogee Velocity     : "
    f"{analysis['apogee_velocity_km_s']:.4f} km/s"
)


print("=" * 60)
ts = load.timescale()

t = ts.now()

latitude, longitude, altitude = satellite_latlon(
    iss,
    t
)

print("\nCURRENT GROUND POSITION")
print("-" * 60)

print(f"Latitude  : {latitude:.4f}°")
print(f"Longitude : {longitude:.4f}°")
print(f"Altitude  : {altitude:.2f} km")

ts = load.timescale()

start_time = ts.now()

period_minutes = analysis["period_minutes"]

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
# Generate ground track
latitudes, longitudes, altitudes = generate_ground_track(
    iss,
    times
)


# Display some ground-track points
print("\nGROUND TRACK SAMPLE")
print("-" * 60)

for i in range(0, 500, 50):
    print(
        f"Lat: {latitudes[i]:8.3f}°   "
        f"Lon: {longitudes[i]:9.3f}°   "
        f"Alt: {altitudes[i]:8.2f} km"
    )
plot_ground_track(
    latitudes,
    longitudes
)   
plot_ground_track_map(
    latitudes,
    longitudes
)
ts = load.timescale()
# Test ground station: Chennai
station_latitude = 13.0827
station_longitude = 80.2707
station_elevation = 0.0

station = create_ground_station(
    station_latitude,
    station_longitude,
    station_elevation
)
observation_time = ts.now()
observation = observe_satellite(
    iss,
    observation_time,
    station,
    station_latitude,
    station_longitude
)
print("\nGROUND STATION OBSERVATION")
print("-" * 60)

print(
    f"Ground Station     : Chennai"
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

skyfield_observation = validate_with_skyfield(
    iss,
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

# Generate prediction times
prediction_times = generate_prediction_times(
    ts,
    observation_time,
    duration_minutes=180,
    step_seconds=10
)

# Calculate elevation profile
elevations = calculate_elevation_profile(
    iss,
    station,
    prediction_times,
    station_latitude,
    station_longitude
)
# Find visibility intervals

elevation_mask_deg = 10.0

visibility_intervals = find_visibility_intervals(
    prediction_times,
    elevations,
    elevation_mask_deg=elevation_mask_deg
)


print("\nPASS PREDICTION")
print("-" * 60)

print(
    f"Prediction window : 180 minutes"
)

print(
    f"Elevation mask    : 0.0°"
)

print(
    f"Passes detected   : "
    f"{len(visibility_intervals)}"
)

for pass_number, (
    start_index,
    end_index
) in enumerate(
    visibility_intervals,
    start=1
):

    max_elevation, max_elevation_time = (
        refine_max_elevation(
            ts,
            iss,
            station,
            station_latitude,
            station_longitude,
            prediction_times,
            elevations,
            start_index,
            end_index
        )
    )
    aos_time, los_time = refine_pass_times(
        ts,
        prediction_times,
        elevations,
        start_index,
        end_index,
        elevation_mask_deg
    )

    duration_seconds = (
        end_index - start_index
    ) * 10

    duration_minutes = (
        duration_seconds / 60
    )

    print(
        f"\nPASS #{pass_number}"
    )

    print(
        f"AOS               : "
        f"{aos_time.utc_strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    print(
        f"Maximum Elevation : "
        f"{max_elevation:.2f}°"
    )

    print(
        f"Max Elevation Time: "
        f"{max_elevation_time.utc_strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    print(
        f"LOS               : "
        f"{los_time.utc_strftime('%Y-%m-%d %H:%M:%S UTC')}"
    )

    print(
        f"Duration          : "
        f"{duration_minutes:.2f} minutes"
    )