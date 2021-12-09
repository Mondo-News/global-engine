"""
This module contains the dash application and is the main entry point to execute the project.
It defines the layout and styling of our web application and also contains the callback functions that provide the
interactivity depending on the user inputs.

Additional CSS files, fonts and other resources are automatically loaded from the "assets" directory in the project folder.
"""
import dash
from utils import utils
from controller.controller import controllerObject
from view.map_viz import viewObject
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# Title of our App for the TAB header in the browser
app.title = 'Mondo News'

server = app.server

# Styling for unpressed/passive button state
black_button_style = {'background-color': 'black',
                      'color': 'white',
                      'height': '45px',
                      'width': '160px',
                      'border': '0px',
                      'margin-left': '0px',
                      'margin-bottom': '0px',
                      'font-family': 'Corbel',
                      'font-size': '12pt',
                      'font-weight': 'bold'}

# Styling for pressed/active button state
white_button_style = {'background-color': 'white',
                      'color': 'black',
                      'height': '45px',
                      'width': '160px',
                      'border': '0px',
                      'margin-left': '0px',
                      'margin-bottom': '0px',
                      'font-family': 'Corbel',
                      'font-size': '16pt',
                      'font-weight': 'bold'}


def serve_layout():
    """
    Contains the layout of the Dash Web Applications. Also triggers initial update of the html map file when page is
    loaded.
    :return: Dash app layout object.
    """
    # Initially refresh map when page is loaded
    viewObject.refreshMap()

    # Define layout and styling of application
    app_layout = html.Div(id='page-content', children=[
        html.Div(children=
                 # HEADER
                 [html.H1('Mondo News', style={'font-size': '56pt',
                                               'font-family': 'Old London',
                                               'margin-bottom': '0px',
                                               'margin-top': '5px',
                                               'padding-bottom': '0px'}),
                  html.P('Your visual global news platform',
                         style={'color': '#968C83',
                                'font-size': '16pt',
                                'font-family': 'Georgia',
                                'font-style': 'italic',
                                'margin-top': '10px',
                                'padding-top': '0px'}),
                  ], style={'text-align': 'center'}),

        # NAVBAR with search bar and buttons
        html.Div(children=
                 # Seach input
                 [dcc.Input(placeholder='Search...', type='text',
                            id='search',
                            debounce=True,
                            style={'width': '350px',
                                   'height': '38px',
                                   'font-family': 'Corbel',
                                   'border': '0px',
                                   'font-size': '14pt',
                                   'color': 'white',
                                   'background-color': 'black',
                                   'margin-bottom': '0',
                                   'margin-top': '1px',
                                   'margin-left': '10px'}),
                  # Buttons
                  html.Button(id='general',
                              children=['General'],
                              n_clicks=0,
                              style=black_button_style
                              ),
                  html.Button(id='technology',
                              children=['Technology'],
                              n_clicks=0,
                              style=black_button_style
                              ),
                  html.Button(id='health',
                              children=['Health'],
                              n_clicks=0,
                              style=black_button_style
                              ),
                  html.Button(id='science',
                              children=['Science'],
                              n_clicks=0,
                              style=black_button_style
                              ),
                  html.Button(id='business',
                              children=['Business'],
                              n_clicks=0,
                              style=black_button_style
                              ),
                  html.Button(id='sports',
                              children=['Sports'],
                              n_clicks=0,
                              style=black_button_style
                              )
                  ], style={'display': 'flex', 'flex-direction': 'row', 'background-color': 'black'}),
        # MAP SECTION
        # dcc.Loading provides the loading wheel when the map is loading
        dcc.Loading(
            id='map-loading',
            children=
            # HTML Iframe is the frame for the folium map that can be passed to the dash app via a .html file that is
            # loaded in Iframe
            [html.Iframe(
                id='map',
                srcDoc=open(utils.path_map_html_file, 'r').read(),
                style={'flex-grow': '1',
                       'height': '80vh',
                       'width': '100%',
                       'margin': '0',
                       'padding': '0'}
            )],
            # Styling of the loading wheel
            type='circle',
            style={'flex-grow': '1',
                   'height': '80vh',
                   'width': '100%',
                   'margin': '0',
                   'padding': '0'},
            color='black'
        ),
        # FOOTER
        html.Table(
            [html.Tr([
                # COLUMN 1: GitHub Logo
                html.Th(
                    html.P(
                        [html.A(
                            [html.Img(
                                src="https://github.com/Mondo-News/global-engine/blob/main/assets/github-logo.png?raw=true",
                                width='60px')],
                            href="https://github.com/Mondo-News/global-engine", target="__blank")],
                        style={'text-align': 'left',
                               'font-family': 'Corbel',
                               'font-size': '12pt'})),
                # COLUMN 2: Text and MailTo Link
                html.Th(
                    html.P(
                        ["Mondo News",
                         html.Br(),
                         "Please reach out via ",
                         html.A(
                             ["Email"],
                             href="mailto:stroebl.benedikt@gmail.com",
                             style={'color': 'black'})],
                        style={'text-align': 'center',
                               'font-family': 'Corbel',
                               'font-size': '12pt'})),
                # Hertie Logo
                html.Th(
                    html.Img(
                        src="https://github.com/Mondo-News/global-engine/blob/main/assets/hertie-logo.png?raw=true",
                        width='200px'), style={'text-align': 'right'})
            ],
            )]
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'font-family': 'Corbel'})

    return app_layout


# Call layout function and assign it to the dash app object
app.layout = serve_layout()


# CALLBACK FUNCTIONS
# Callbacks listen to user actions/inputs and trigger methods
# Below six methods change button styling (black/white) when clicked
@app.callback(Output('general', 'style'), [Input('general', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    # This first method is slightly different, since it listens to the "general" button and return the inverse
    # styling to the other buttons
    if (n_clicks % 2) != 0:
        return black_button_style
    else:
        return white_button_style


@app.callback(Output('technology', 'style'), [Input('technology', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    # If button is clicked an odd number of times that its passive; return black styling. Else, return white styling
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('health', 'style'), [Input('health', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('science', 'style'), [Input('science', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('business', 'style'), [Input('business', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('sports', 'style'), [Input('sports', 'n_clicks')])
def change_button_style(n_clicks):
    """
    Listens to button clicks and returns styling objects based on whether buttons was already active or not.
    :param n_clicks: Number of time button has been clicked since page was loaded.
    :return: Style object based on button active/passive
    """
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


# Method below triggers the whole map updating and data filtering based on user input (categories; search)
@app.callback(Output('map', 'srcDoc'),
              [Input('general', 'n_clicks'),
               Input('technology', 'n_clicks'),
               Input('health', 'n_clicks'),
               Input('science', 'n_clicks'),
               Input('business', 'n_clicks'),
               Input('sports', 'n_clicks'),
               Input('search', 'value')])
def update_map(general_n_clicks, technology_n_clicks, health_n_clicks, science_n_clicks, business_n_clicks,
               sports_n_clicks, query_string):
    """
    Listens to all buttons and the search input field whether they are clicked/text is entered and triggers the update
    process of the map depending on the input.
    :param general_n_clicks: Number of clicks of the "general" buttons
    :param technology_n_clicks: Number of clicks of the "technology" buttons
    :param health_n_clicks: Number of clicks of the "health" buttons
    :param science_n_clicks: Number of clicks of the "science" buttons
    :param business_n_clicks: Number of clicks of the "business" buttons
    :param sports_n_clicks: Number of clicks of the "sports" buttons
    :param query_string: Text entered in the search field
    :return: Either dash.no_update OR the srcDoc with the newly rendered .html folium map used in the Iframe component.
    """

    # The callback context object contains information about the state of all components in the application
    ctx = dash.callback_context

    # Category Update
    for prop in ctx.inputs.keys():
        # If there was no text search performed by the user
        if "search.value" != prop:
            # Cut category string from property name in dash context object
            id = prop[:len(prop) - 9]
            # If there has been an input for this property
            if ctx.inputs[prop] is not None:
                # Select/Deselect category
                # (special case for "general"-button with inverse calling of categorSelect methods)
                if prop == "general.n_clicks":
                    if (ctx.inputs[prop] % 2) != 0:
                        controllerObject.deselectCategory(id)
                    else:
                        controllerObject.selectCategory(id)
                else:
                    if (ctx.inputs[prop] % 2) != 0:
                        controllerObject.selectCategory(id)
                    else:
                        controllerObject.deselectCategory(id)

    # Map Refresh
    print('New keyword search with query: ' + str(query_string))
    # If there was no text search then trigger the refresh method without query string input
    if query_string == '' or query_string is None:
        viewObject.refreshMap()
    else:
        viewObject.refreshMap(query_string)

    # When page is loaded and all buttons are unclicked; search string is None then dont return new map object.
    # This is necessary since Dash always calls callback methods on page load
    if general_n_clicks == technology_n_clicks == health_n_clicks == science_n_clicks == business_n_clicks == sports_n_clicks == 0 and query_string is None:
        return dash.no_update
    else:
        return open(utils.path_map_html_file, 'r').read()


# Start app
if __name__ == '__main__':
    app.run_server(debug=True)
