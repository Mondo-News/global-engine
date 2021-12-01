import json
import urllib
import webbrowser
import folium
from controller.controller import controllerObject


class View:

    def __init__(self):
        # Setting up the world countries data URL
        url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        country_shapes = f'{url}/world-countries.json'
        jsonurl = urllib.request.urlopen(country_shapes)
        self.country_json_data = json.loads(jsonurl.read())  # <-- read from it

    def styleFuntion(self, feature):
        """
        Styling for choropleth map when not-hovering.
        Returns different styling for countries where there is news data available and where there is not
        :param feature: GEOJson feature
        :return: folium style dict
        """
        style_no_data = {'fillColor': '#968C83',
                         'color': '#000000',
                         'fillOpacity': 0.2,
                         'weight': 0.1}
        style_data = {'fillColor': '#BA0020',
                      'color': '#000000',
                      'fillOpacity': 0.7,
                      'weight': 0.1}

        if feature['id'].lower() in controllerObject.getAvailableIsoCodes():
            return style_data
        else:
            return style_no_data

    def highlightFunction(self, feature):
        """
        Styling for choropleth map when mouse is hovering
        :param feature: GEOJson feature
        :return: folium style dict
        """
        return {'fillColor': '#000000',
                'color': '#000000',
                'fillOpacity': 0.50,
                'weight': 0.1}

    def buildPopupHTMLArticleTable(self, three_letter_iso_id):
        """
        For a given country 3-Letter ISO this method build the HTML string for the folium Popup need in load_map()
        :return: HTML String
        """

        html_table = f"""
                <table>
                    <tr>
                        <th>Thumbnail</th>
                        <th>Title</th>
                        <th>Outlet</th>
                    </tr>
        """

        df = controllerObject.getTopArticles()
        df = df[df['country'].str.lower() == three_letter_iso_id.lower()]
        if three_letter_iso_id == "deu" or three_letter_iso_id == "usa":  # TODO: Delete
            print("Country name: " + three_letter_iso_id)
            print("Filtered DF: " + df.head(5))
        for index, row in df.iterrows():
            html_table_row = f"""<tr>
                <td><img class="thumbnail" src={row['urlToImage']}></td>
                <td><a href={row['url']} target="_blank">{row['title']}</a></td>
                <td><img class="outlet-logo" src="https://upload.wikimedia.org/wikipedia/commons/f/fb/Cnn_logo_red_background.png"></td>
            </tr>
            """
            html_table = html_table + html_table_row

        return html_table + "</table>"

    def load_map(self):
        """
        Creates and renders folium/leaflet map.
        :return: folium map object
        """
        # Create a map
        m1 = folium.Map(location=[52.51284693487173, 13.389233110107703], tiles='cartodbpositron', zoom_start=3)

        # add marker one by one on the map
        for i in range(len(self.country_json_data['features'])):
            # html_table = self.buildPopupHTMLArticleTable(self.country_json_data['features'][i]['id']) # TODO: Decomment
            html_table = ""  # TODO:delete
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
                <h1>{self.country_json_data['features'][i]['properties']['name']}</h1>
                <h2>What people talk about:</h2>
            """ + \
                   html_table + \
                   f"</body>"

            iframe = folium.IFrame(html=html, width=640, height=450)
            popup = folium.Popup(iframe, max_width=2650)
            geoj = folium.GeoJson(
                self.country_json_data['features'][i],
                name="geojson",
                zoom_on_click=True,
                style_function=self.styleFuntion,
                highlight_function=self.highlightFunction
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
