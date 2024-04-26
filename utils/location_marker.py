import folium


def mark_location(latitude, longitude):

    m = folium.Map([latitude, longitude], zoom_start=12)

    folium.Marker(
        location=[latitude, longitude],
        tooltip="Your child was most recently found here",
        popup=f"Location\n- Latitude: {longitude} \n- Longitude:{longitude} ",
        icon=folium.Icon(icon="cloud"),
    ).add_to(m)

    m.save("templates/map.html")
