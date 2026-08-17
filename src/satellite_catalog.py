from pathlib import Path

from src.tle_loader import load_satellite_from_file


def find_tle_files(
    tle_directory
):
    """
    Find all TLE files inside
    the specified directory.
    """

    tle_path = Path(
        tle_directory
    )

    tle_files = sorted(
        tle_path.glob("*.tle")
    )

    return tle_files


def load_satellite_catalog(
    tle_directory
):
    """
    Load all satellites from all
    TLE files in a directory.

    Returns a dictionary:

        satellite_name -> satellite_object
    """

    tle_files = find_tle_files(
        tle_directory
    )

    if not tle_files:

        raise FileNotFoundError(
            f"No TLE files found in "
            f"{tle_directory}"
        )

    catalog = {}

    for tle_file in tle_files:

        satellites = (
            load_satellite_from_file(
                str(tle_file)
            )
        )

        for satellite in satellites:

            catalog[satellite.name] = {
                "satellite": satellite,
                "tle_file": str(tle_file)
            }

    return catalog


def print_satellite_catalog(
    catalog
):
    """
    Display all satellites
    available in the catalog.
    """

    print(
        "\nAVAILABLE SATELLITES"
    )

    print(
        "-" * 60
    )

    for index, (
        name,
        information
    ) in enumerate(
        catalog.items(),
        start=1
    ):

        print(
            f"{index}. {name}"
        )

        print(
            f"   TLE File: "
            f"{information['tle_file']}"
        )

    print(
        "-" * 60
    )

def select_satellite(
    catalog,
    selection
):
    """
    Select a satellite from the catalog.

    The selection can be either:
    - an integer index
    - an exact satellite name
    """

    # --------------------------------------------------
    # Selection by number
    # --------------------------------------------------

    if isinstance(selection, int):

        satellite_names = list(
            catalog.keys()
        )

        if selection < 1 or selection > len(
            satellite_names
        ):
            raise ValueError(
                "Invalid satellite selection."
            )

        selected_name = satellite_names[
            selection - 1
        ]

        return catalog[
            selected_name
        ]["satellite"]

    # --------------------------------------------------
    # Selection by satellite name
    # --------------------------------------------------

    if isinstance(selection, str):

        if selection not in catalog:
            raise ValueError(
                f"Satellite '{selection}' "
                f"not found in catalog."
            )

        return catalog[
            selection
        ]["satellite"]

    # --------------------------------------------------
    # Invalid selection type
    # --------------------------------------------------

    raise TypeError(
        "Selection must be an integer "
        "or satellite name."
    )