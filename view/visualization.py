import json
import urllib
import webbrowser
import folium
import controller


class View:

    def __init__(self):
        # Setting up the world countries data URL
        url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        country_shapes = f'{url}/world-countries.json'
        jsonurl = urllib.request.urlopen(country_shapes)
        self.country_json_data = json.loads(jsonurl.read())  # <-- read from it

        # Styling for choropleth map when not-hovering
        self.style_function = lambda x: {'fillColor': '#ffffff',
                                         'color': '#000000',
                                         'fillOpacity': 0.1,
                                         'weight': 0.1}

        # Styling for choropleth map when mouse is hovering
        self.highlight_function = lambda x: {'fillColor': '#000000',
                                             'color': '#000000',
                                             'fillOpacity': 0.50,
                                             'weight': 0.1}

    def load_map(self):
        """
        Creates and renders folium/leaflet map.
        :return: folium map object
        """
        # Create a map
        m1 = folium.Map(location=[52.51284693487173, 13.389233110107703], tiles='cartodbpositron', zoom_start=3)

        # add marker one by one on the map
        for i in range(len(self.country_json_data['features'])):
            html = f"""
            <style>
                body {{
                    font-family: Corbel;
                }}

                h1 {{
                    font-size: 20px;
                }}

                h2 {{
                    font-size: 14px;
                }}

                table {{
                    font-size: 14px;
                    width: 600px;
                    border-spacing: 10px;
                }}

                th {{
                    border-bottom: 1px solid black;
                    padding: 5px;
                }}

                .thumbnail {{
                    width: 100;
                }}

                .outlet-logo {{
                    width: 50;
                }}

                a {{
                color: black;
                text-decoration: none;
                }}

                a:hover {{
                    text-decoration: underline;
                }}

                p {{
                    color: red;
                }}

            </style>

            <body>
                <h1> {self.country_json_data['features'][i]['properties']['name']}</h1>
                <h2>What people talk about:</h2>
                <table>
                    <tr>
                        <th>Thumbnail</th>
                        <th>Title</th>
                        <th>Outlet</th>
                    </tr>
                    <tr>
                        <td><img class="thumbnail" src="https://s.abcnews.com/images/International/uk-gty-er-211127_1638029361181_hpMain_16x9_608.jpg"></td>
                        <td>COVID-19 live updates: Omicron cases spread to UK, Germany</td>
                        <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/American_Broadcasting_Company_Logo.svg/2044px-American_Broadcasting_Company_Logo.svg.png"></td>
                    </tr>
                    <tr>
                        <td><img class="thumbnail" src="https://a57.foxnews.com/hp.foxnews.com/images/2021/11/1280/533/6d04833942cf467c56742c487d7e0540.jpg?tl=1&ve=1"></td>
                        <td>Waukesha victim's uncle, a vet who served in Iraq, reveals what he wants to happen to the suspect</td>
                        <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/de/thumb/6/67/Fox_News_Channel_logo.svg/1920px-Fox_News_Channel_logo.svg.png"></td>
                    </tr>
                    <tr>
                        <td><img class="thumbnail" src="https://cdn.cnn.com/cnnnext/dam/assets/211127130931-covid-omicron-vaccine-inequity-112721-large-tease.jpg"></td>
                        <td>Scientists: Vaccine inequity and hesitancy to blame for variant</td>
                        <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Cnn_logo_red_background.png"></td>
                    </tr>
                    <tr>
                        <td><img class="thumbnail" src="https://s.abcnews.com/images/International/WireAP_b90b43f0101a4a2c86236ca17761eb9c_16x9_992.jpg"></td>
                        <td>Nissan investing in electric vehicles, battery development</td>
                        <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/American_Broadcasting_Company_Logo.svg/2044px-American_Broadcasting_Company_Logo.svg.png"></td>
                    </tr>
                    <tr>
                        <td><img class="thumbnail" src="https://cdn.cnn.com/cnnnext/dam/assets/211128135909-01-virgil-abloh-file-070521-medium-tease.jpg"></td>
                        <td><a href="https://edition.cnn.com/style/article/virgil-abloh-death/index.html" target="_blank">Louis Vuitton artistic director Virgil Abloh dies at 41</a></td>
                        <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Cnn_logo_red_background.png"></td>
                    </tr>
                </table>
            </body>
                """
            iframe = folium.IFrame(html=html, width=640, height=450)
            popup = folium.Popup(iframe, max_width=2650)
            geoj = folium.GeoJson(
                self.country_json_data['features'][i],
                name="geojson",
                zoom_on_click=True,
                highlight_function=self.highlight_function
            )
            popup.add_to(geoj)
            geoj.add_to(m1)
        return m1


def auto_open(path, map_object):
    """
    Creates HTML file of map_object and automatically opens it in default web browser.
    :param path: Path, where HTML file will be created
    :param map_object: Map Object to be saved and opened
    :return: None
    """
    html_page = f"{path}"
    map_object.save(html_page)
    # open in browser.
    new = 2
    webbrowser.open(html_page, new=new)


# Instantiate a View() object
viewObject = View()
# Create map and open it
auto_open("map.html", viewObject.load_map())

# OLD CODE BELOW
# # add marker one by one on the map
# for i in range(0, len(data)):
#     html = f"""
#         <h1> {data.iloc[i]['name']}</h1>
#         <p>You can use any html here! Let's do a list:</p>
#         <ul>
#             <li>Item 1</li>
#             <li>Item 2</li>
#         </ul>
#         </p>
#         <p>And that's a <a href="https://www.python-graph-gallery.com">link</a></p>
#         """
#     iframe = folium.IFrame(html=html, width=200, height=200)
#     popup = folium.Popup(iframe, max_width=2650)
#     folium.Marker(
#         location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
#         popup=popup,
#         icon=folium.DivIcon(html=f"""
#             <div><svg>
#                 <circle cx="50" cy="50" r="40" fill="#69b3a2" opacity=".4"/>
#                 <rect x="35", y="35" width="30" height="30", fill="red", opacity=".3"
#             </svg></div>""")
#     ).add_to(m1)
