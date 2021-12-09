import json
import urllib
import webbrowser
import folium
from controller.controller import controllerObject
from utils import utils
import ssl


class View:

    def __init__(self):
        # Setting up the world COUNTRIES data URL
        countries_url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        countries_jsonurl = f'{countries_url}/world-countries.json'
        country_shapes = urllib.request.urlopen(countries_jsonurl)
        self.country_json_data = json.loads(country_shapes.read())  # <-- read from it

        # Setting up the world CAPITALS data URL
        capitals_url = 'http://www.geognos.com/api/en/countries/info'
        capitals_jsonurl = urllib.request.urlopen(f'{capitals_url}/all.json')
        self.capitals_json_data = json.loads(capitals_jsonurl.read())

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

        if feature['id'].lower() in controllerObject.getAvailableIsoCodes(3):
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

    def buildPopupHTMLArticleTable(self, three_letter_iso_id, selected_categories, query_string=None):
        """
        For a given country 3-Letter ISO this method build the HTML string for the folium Popup need in load_map()
        :return: HTML String
        """

        # URLs to category images for third column in popup
        category_image_urls = {
            'general': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/general.png?raw=true',
            'business': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/business.png?raw=true',
            'technology': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/technology.png?raw=true',
            'science': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/science.png?raw=true',
            'health': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/health.png?raw=true',
            'sports': 'https://github.com/Mondo-News/global-engine/blob/main/data/pictures/sports.png?raw=true'
        }

        html_table = f"""
                <table>
                    <tr>
                        <th>Thumbnail</th>
                        <th>Title</th>
                        <th>Category</th>
                    </tr>
        """
        assert len(three_letter_iso_id) == 3

        # Choose how to filter article data for HTML popup
        if query_string == '' or query_string is None:
            df_filtered_articles = controllerObject.getArticlesByCategories(selected_categories)
        else:
            df_filtered_articles = controllerObject.getArticlesByKeywordSearch(selected_categories, query_string)

        df_filtered_articles = df_filtered_articles[
            df_filtered_articles['country'].str.lower() == three_letter_iso_id.lower()]
        if three_letter_iso_id == "deu" or three_letter_iso_id == "usa":  # TODO: Delete
            print("Country name: " + three_letter_iso_id)
            print("Filtered DF: " + df_filtered_articles.head(5))
        for index, row in df_filtered_articles.iterrows():
            html_table_row = f"""<tr>
                <td><img class="thumbnail" src={row['urlToImage']}></td>
                <td><a href={row['url']} target="_blank">{row['title']}</a></td>
                <td style="text-align: center;"><img class="outlet-logo" src={category_image_urls[row['category']]}></td>
            </tr>
            """
            html_table = html_table + html_table_row

        return html_table + "</table>"

    def load_map(self, selected_categories, query_string=None):
        """
        Creates and renders folium/leaflet map.
        :return: folium map object
        """
        # Create a map
        m1 = folium.Map(location=[52.51284693487173, 13.389233110107703], tiles='cartodbpositron', zoom_start=3)

        # Refresh Data in model from CSV
        controllerObject.refreshDataFromSQL()

        # add marker one by one on the map
        for i in range(len(self.country_json_data['features'])):
            html_table = self.buildPopupHTMLArticleTable(self.country_json_data['features'][i]['id'],
                                                         selected_categories, query_string)
            html = f"""
            <style>
                @font-face {{
                font-family: 'Corbel';
                src: url('/Corbel.eot');
                src: url('/Corbel.eot?#iefix') format('embedded-opentype'),
                    url('/Corbel.woff2') format('woff2'),
                    url('/Corbel.woff') format('woff'),
                    url('/Corbel.ttf') format('truetype'),
                    url('/Corbel.svg#Corbel') format('svg');
                font-weight: normal;
                font-style: normal;
                font-display: swap;
                }}
                
                @font-face {{
                font-family: 'Old London';
                src: url('/OldLondon.woff2') format('woff2'),
                    url('/OldLondon.woff') format('woff');
                font-weight: normal;
                font-style: normal;
                font-display: swap;
                }}

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
                    width: 30;
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
                # zoom_on_click=True,
                style_function=self.styleFuntion,
                highlight_function=self.highlightFunction
            )
            popup.add_to(geoj)
            geoj.add_to(m1)

            # Create Marker on Capital for countries where we have geo data of capital
            capital_location = self.getCapitalLocation(self.country_json_data['features'][i]['id'])
            if capital_location is not None:
                folium.CircleMarker(
                    location=self.getCapitalLocation(self.country_json_data['features'][i]['id']),
                    radius=1,
                    color="#3186cc",
                    fill=True,
                    fill_color="#3186cc"
                ).add_to(m1)

        return m1

    def getCapitalLocation(self, country_iso_code):
        # Check whether ISO code of source database is 2 or 3-Letters and convert if 3-Letter
        if len(country_iso_code) > 2:
            country_iso_code = utils.convertIsoCodes_3_to_2(country_iso_code).upper()

        # Return None if there is no news data for the requested country
        if country_iso_code.lower() not in controllerObject.getAvailableIsoCodes(2):
            return None

        # Get Capital location tupel and except Type or Key Errors for countries where there is no geo data available
        try:
            capital_location = self.capitals_json_data['Results'][country_iso_code]['Capital']['GeoPt']
            return capital_location
        except TypeError:
            return None
        except KeyError:
            print("KeyError: " + country_iso_code)
            return None

    def saveMapHTML(self, map_object):
        path = utils.path_map_html_file
        map_object.save(path)

    def refreshMap(self, query_string=None):
        print('New map is loading...')
        loaded_map_object = self.load_map(controllerObject.getSelectedCategories(), query_string)
        print("Refreshed map.html has been created")
        self.saveMapHTML(loaded_map_object)


def auto_open(map_object):
    """
    Creates HTML file of map_object and automatically opens it in default web browser.
    :param path: Path, where HTML file will be created
    :param map_object: Map Object to be saved and opened
    :return: None
    """
    map_object.save(utils.path_map_html_file)
    # open in browser.
    new = 2
    webbrowser.open(utils.path_map_html_file, new=new)


# Instantiate a View() object
viewObject = View()
# Create map and open it
# auto_open(viewObject.load_map(controllerObject.getSelectedCategories())) # TODO: Delete
