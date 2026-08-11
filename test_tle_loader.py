from src.tle_loader import load_satellite_from_file


satellites = load_satellite_from_file(
    "data/tle/iss.txt"
)


for satellite in satellites:

    print("Satellite:", satellite.name)

    print("\nTLE Line 1:")
    print(satellite.tle_line1)

    print("\nTLE Line 2:")
    print(satellite.tle_line2)