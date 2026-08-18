# ============================================================
# SATELLITE PROFILE
# ============================================================


def build_satellite_profile(
    satellite,
    analysis,
    classification,
    validation,
    tle_file=None
):
    """
    Build a structured engineering profile
    for a satellite.
    """

    profile = {
        "name": satellite.name,

        "tle_file": tle_file,

        "orbital_elements": {
            "inclination_deg":
                analysis["inclination_deg"],

            "raan_deg":
                analysis["raan_deg"],

            "eccentricity":
                analysis["eccentricity"],

            "argument_of_perigee_deg":
                analysis[
                    "argument_of_perigee_deg"
                ],

            "mean_anomaly_deg":
                analysis[
                    "mean_anomaly_deg"
                ],

            "mean_motion_rev_day":
                analysis[
                    "mean_motion_rev_day"
                ]
        },

        "derived_parameters": {
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

            "perigee_radius_km":
                analysis[
                    "perigee_radius_km"
                ],

            "apogee_radius_km":
                analysis[
                    "apogee_radius_km"
                ],

            "perigee_altitude_km":
                analysis[
                    "perigee_altitude_km"
                ],

            "apogee_altitude_km":
                analysis[
                    "apogee_altitude_km"
                ],

            "perigee_velocity_km_s":
                analysis[
                    "perigee_velocity_km_s"
                ],

            "apogee_velocity_km_s":
                analysis[
                    "apogee_velocity_km_s"
                ]
        },

        "classification": classification,

        "validation": validation
    }

    return profile


def print_satellite_profile(
    profile
):
    """
    Display a professional satellite
    engineering profile.
    """

    print("\n" + "=" * 60)

    print(
        "                 SATELLITE PROFILE"
    )

    print("=" * 60)

    print(
        f"Satellite          : "
        f"{profile['name']}"
    )

    if profile["tle_file"]:

        print(
            f"TLE Source         : "
            f"{profile['tle_file']}"
        )

    print("\nORBIT CLASSIFICATION")

    print("-" * 60)

    classification = (
        profile["classification"]
    )

    print(
        f"Altitude Class     : "
        f"{classification['altitude_class']}"
    )

    print(
        f"Period Class       : "
        f"{classification['period_class']}"
    )

    print(
        f"Eccentricity Class : "
        f"{classification['eccentricity_class']}"
    )

    print(
        f"Inclination Class  : "
        f"{classification['inclination_class']}"
    )

    print("\nORBITAL STATUS")

    print("-" * 60)

    validation = (
        profile["validation"]
    )

    print(
        f"Data Valid         : "
        f"{validation['valid']}"
    )

    if validation["warnings"]:

        print("\nWarnings:")

        for warning in (
            validation["warnings"]
        ):

            print(
                f"- {warning}"
            )

    if validation["errors"]:

        print("\nErrors:")

        for error in (
            validation["errors"]
        ):

            print(
                f"- {error}"
            )

    print("\nKEY PARAMETERS")

    print("-" * 60)

    parameters = (
        profile["derived_parameters"]
    )

    print(
        f"Altitude           : "
        f"{parameters['altitude_km']:.2f} km"
    )

    print(
        f"Orbital Period     : "
        f"{parameters['period_minutes']:.2f} min"
    )

    print(
        f"Perigee Altitude   : "
        f"{parameters['perigee_altitude_km']:.2f} km"
    )

    print(
        f"Apogee Altitude    : "
        f"{parameters['apogee_altitude_km']:.2f} km"
    )

    print(
        f"Perigee Velocity   : "
        f"{parameters['perigee_velocity_km_s']:.4f} km/s"
    )

    print(
        f"Apogee Velocity    : "
        f"{parameters['apogee_velocity_km_s']:.4f} km/s"
    )

    print("=" * 60)