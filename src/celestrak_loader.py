import os
import re
from urllib.parse import urlencode
from urllib.request import urlopen


CELESTRAK_URL = (
    "https://celestrak.org/NORAD/elements/gp.php"
)


# ============================================================
# PARSE TLE TEXT
# ============================================================

def parse_tle_text(tle_text):
    """
    Parse CelesTrak 3LE/TLE text.

    Returns:
        list of tuples:
        (satellite_name, line1, line2)
    """

    lines = [
        line.strip()
        for line in tle_text.splitlines()
        if line.strip()
    ]

    satellites = []

    index = 0

    while index + 2 < len(lines):

        name = lines[index]
        line1 = lines[index + 1]
        line2 = lines[index + 2]

        if (
            line1.startswith("1 ")
            and
            line2.startswith("2 ")
        ):

            satellites.append(
                (
                    name,
                    line1,
                    line2
                )
            )

            index += 3

        else:

            index += 1

    return satellites


# ============================================================
# SAVE TLE SETS
# ============================================================

def save_tle_sets(
    tle_sets,
    output_directory="data/tle"
):
    """
    Save parsed TLE sets as individual .tle files.
    """

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    saved_files = []

    for (
        name,
        line1,
        line2
    ) in tle_sets:

        clean_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            name
        ).strip("_")

        if not clean_name:

            clean_name = (
                f"satellite_{len(saved_files) + 1}"
            )

        filepath = os.path.join(
            output_directory,
            f"{clean_name}.tle"
        )

        with open(
            filepath,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                f"{name}\n"
            )

            file.write(
                f"{line1}\n"
            )

            file.write(
                f"{line2}\n"
            )

        saved_files.append(
            filepath
        )

    return saved_files


# ============================================================
# DOWNLOAD CELESTRAK GROUP
# ============================================================

def download_celestrak_group(
    group_name,
    output_directory="data/tle"
):
    """
    Download a CelesTrak satellite group
    and save its TLEs.
    """

    query = urlencode(
        {
            "GROUP": group_name,
            "FORMAT": "TLE"
        }
    )

    url = (
        f"{CELESTRAK_URL}?{query}"
    )

    try:

        with urlopen(
            url,
            timeout=15
        ) as response:

            tle_text = response.read().decode(
                "utf-8"
            )

    except Exception as error:

        raise RuntimeError(
            f"CelesTrak connection failed.\n"
            f"URL: {url}\n"
            f"Reason: {error}"
        )

    tle_sets = parse_tle_text(
        tle_text
    )

    if not tle_sets:

        raise RuntimeError(
            "CelesTrak returned no valid TLE sets."
        )

    return save_tle_sets(
        tle_sets,
        output_directory
    )