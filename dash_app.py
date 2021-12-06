import dash
from utils import utils
from controller.controller import controllerObject
from view.map_viz import viewObject
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

server = app.server

black_button_style = {'background-color': 'black',
                      'color': 'white',
                      'height': '45px',
                      'width': '160px',
                      'border': '0px',
                      'margin-left': '0px',
                      'margin-bottom': '0px',
                      'font-family': 'corbel',
                      'font-size': '12pt',
                      'font-weight': 'bold'}

white_button_style = {'background-color': 'white',
                      'color': 'black',
                      'height': '45px',
                      'width': '160px',
                      'border': '0px',
                      'margin-left': '0px',
                      'margin-bottom': '0px',
                      'font-family': 'corbel',
                      'font-size': '16pt',
                      'font-weight': 'bold'}


def serve_layout():
    app_layout = html.Div(children=[
        html.Div(children=[
            html.H1('Mondo News', style={'font-size': '56pt',
                                         'font-family': 'old london',
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

        html.Div(children=[
            dcc.Input(placeholder='Search...', type='text',
                      id='search',
                      debounce=True,
                      style={'width': '350px',
                             'height': '38px',
                             'font-family': 'corbel',
                             'border': '0px',
                             'font-size': '14pt',
                             'color': 'white',
                             'background-color': 'black',
                             'margin-bottom': '0',
                             'margin-top': '1px',
                             'margin-left': '10px'}),
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
        dcc.Loading(
            id='map-loading',
            children=[html.Iframe(
                id='map',
                srcDoc=open(utils.path_map_html_file, 'r').read(),
                style={'flex-grow': '1',
                       'height': '80vh',
                       'width': '100%',
                       'margin': '0',
                       'padding': '0'}
            )],
            type='circle',
            style={'flex-grow': '1',
                   'height': '80vh',
                   'width': '100%',
                   'margin': '0',
                   'padding': '0'},
            color='black'
        ),
        html.Div(id='hidden-div1', style={'display': 'none'}),
        html.Div(id='hidden-div2', style={'display': 'none'}),
        html.Div(id='hidden-div3', style={'display': 'none'}),
        html.Div(id='hidden-div4', style={'display': 'none'}),
        html.Div(id='hidden-div5', style={'display': 'none'}),
        html.Div(id='hidden-div6', style={'display': 'none'}),
        html.Div(id='hidden-div7', style={'display': 'none'}),
        html.Table(
            [html.Tr([
                html.Th(html.P([html.A([html.Img(
                    src="https://github.com/Mondo-News/global-engine/blob/main/assets/github-logo.png?raw=true",
                    width='60px')],
                    href="https://github.com/Mondo-News/global-engine", target="__blank")],
                    style={'text-align': 'left',
                           'font-family': 'corbel',
                           'font-size': '12pt'})),
                html.Th(html.P(["Mondo News",
                                html.Br(),
                                "Please reach out via ",
                                html.A(["Email"], href="mailto:stroebl.benedikt@gmail.com", style={'color': 'black'})],
                               style={'text-align': 'center',
                                      'font-family': 'corbel',
                                      'font-size': '12pt'})),
                html.Th(html.Img(
                    src="https://github.com/Mondo-News/global-engine/blob/main/assets/hertie-logo.png?raw=true",
                    width='200px'), style={'text-align': 'right'})
            ],
            )]
        )
    ], style={'display': 'flex', 'flex-direction': 'column', 'font-family': 'corbel'})
    return app_layout


app.layout = serve_layout()


@app.callback(Output('general', 'style'), [Input('general', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return black_button_style
    else:
        return white_button_style


@app.callback(Output('technology', 'style'), [Input('technology', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('health', 'style'), [Input('health', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('science', 'style'), [Input('science', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('business', 'style'), [Input('business', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


@app.callback(Output('sports', 'style'), [Input('sports', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return black_button_style


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
    ctx = dash.callback_context

    # Category Update
    for prop in ctx.inputs.keys():
        if "search.value" != prop:
            id = prop[:len(prop) - 9]
            if ctx.inputs[prop] is not None:
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
    if query_string == '' or query_string is None:
        print("Used method with emtpy query string input")
        viewObject.refreshMap('')
    else:
        print("Used method with query string input")
        viewObject.refreshMap(query_string)

    if general_n_clicks == technology_n_clicks == health_n_clicks == science_n_clicks == business_n_clicks == sports_n_clicks == 0 and query_string is None:
        return dash.no_update
    else:
        return open(utils.path_map_html_file, 'r').read()


if __name__ == '__main__':
    app.run_server(debug=True)
