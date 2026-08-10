import matplotlib.pyplot as plt
import plotly.graph_objects as go


def plot_ground_track(latitudes, longitudes):
    """
    Plot satellite ground track using
    latitude and longitude with Matplotlib.
    """

    plt.figure(figsize=(12, 6))

    plt.plot(
        longitudes,
        latitudes
    )

    plt.xlabel("Longitude (degrees)")
    plt.ylabel("Latitude (degrees)")

    plt.title("ISS Ground Track")

    plt.grid(True)

    plt.xlim(-180, 180)
    plt.ylim(-90, 90)

    plt.show()


def plot_ground_track_map(latitudes, longitudes):
    """
    Plot the satellite ground track on an
    interactive world map using Plotly.
    """

    figure = go.Figure()

    figure.add_trace(
        go.Scattergeo(
            lat=latitudes,
            lon=longitudes,
            mode="lines",
            name="ISS Ground Track",
            line=dict(width=2)
        )
    )

    figure.update_geos(
        projection_type="equirectangular",
        showland=True,
        showocean=True,
        showcountries=True,
        showcoastlines=True,
        coastlinecolor="black",
        landcolor="lightgray",
        oceancolor="lightblue"
    )

    figure.update_layout(
        title="ISS Ground Track — One Orbital Period",
        height=600,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    figure.show()