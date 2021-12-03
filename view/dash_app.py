import dash
from controller.controller import controllerObject
from view.visualization import viewObject
from dash import html, dcc
from dash.dependencies import Input, Output
import time

app = dash.Dash(__name__)

white_button_style = {'background-color': 'white',
                      'color': 'black',
                      'height': '45px',
                      'width': '120px',
                      'margin-left': '50px',
                      'margin-bottom': '20px',
                      'font-family': 'Corbel',
                      'font-size': '12pt',
                      'border-radius': '5px'}

red_button_style = {'background-color': '#BA0020',
                    'color': 'white',
                    'height': '45px',
                    'width': '120px',
                    'margin-left': '50px',
                    'margin-bottom': '20px',
                    'font-family': 'Corbel',
                    'font-size': '16pt',
                    'border-radius': '5px'}

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Mondo News', style={'font-size': '56pt',
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

    html.Div(children=[
        dcc.Input(value='Search...', type='text',
                  style={'width': '300px',
                         'height': '30px',
                         'font-family': 'Corbel',
                         'color': 'grey',
                         'margin-bottom': '20px',
                         'margin-top': '5px',
                         'margin-left': '20px'}),
        html.Button(id='general',
                    children=['general'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='technology',
                    children=['Technology'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='health',
                    children=['Health'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='science',
                    children=['Science'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='business',
                    children=['Business'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='sports',
                    children=['Sports'],
                    n_clicks=0,
                    style=white_button_style
                    )
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Iframe(
        id='map',
        srcDoc=open('map.html', 'r').read(),
        style={
            'flex-grow': '1',
            'height': '80vh',
            'margin': '0',
            'padding': '0'}
    ),
    html.Div(id='hidden-div1', style={'display': 'none'}),
    html.Div(id='hidden-div2', style={'display': 'none'}),
    html.Div(id='hidden-div3', style={'display': 'none'}),
    html.Div(id='hidden-div4', style={'display': 'none'}),
    html.Div(id='hidden-div5', style={'display': 'none'}),
    html.Div(id='hidden-div6', style={'display': 'none'})

], style={'display': 'flex', 'flex-direction': 'column', 'font-family': 'Corbel'})


@app.callback(
    dash.dependencies.Output('map', 'srcDoc'),
    [dash.dependencies.Input('general', 'n_clicks'),
     dash.dependencies.Input('technology', 'n_clicks'),
     dash.dependencies.Input('health', 'n_clicks'),
     dash.dependencies.Input('science', 'n_clicks'),
     dash.dependencies.Input('business', 'n_clicks'),
     dash.dependencies.Input('sports', 'n_clicks')])
def update_map(general_n_clicks, technology_n_clicks, health_n_clicks, science_n_clicks, business_n_clicks, sports_n_clicks):
    viewObject.refreshMap()
    if general_n_clicks == technology_n_clicks == health_n_clicks == science_n_clicks == business_n_clicks == sports_n_clicks == 0:
        return dash.no_update
    else:
        return open('map.html', 'r').read()


@app.callback(Output('general', 'style'), [Input('general', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return white_button_style
    else:
        return red_button_style


@app.callback(Output('technology', 'style'), [Input('technology', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('health', 'style'), [Input('health', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('science', 'style'), [Input('science', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('business', 'style'), [Input('business', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('sports', 'style'), [Input('sports', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('hidden-div1', 'children'), inputs=[Input('general', 'n_clicks'), Input('general', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.deselectCategory(id)
    else:
        controllerObject.selectCategory(id)
    return id


@app.callback(Output('hidden-div2', 'children'), inputs=[Input('technology', 'n_clicks'), Input('technology', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.selectCategory(id)
    else:
        controllerObject.deselectCategory(id)
    return id


@app.callback(Output('hidden-div3', 'children'), inputs=[Input('business', 'n_clicks'), Input('business', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.selectCategory(id)
    else:
        controllerObject.deselectCategory(id)
    return id


@app.callback(Output('hidden-div4', 'children'), inputs=[Input('health', 'n_clicks'), Input('health', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.selectCategory(id)
    else:
        controllerObject.deselectCategory(id)
    return id


@app.callback(Output('hidden-div5', 'children'), inputs=[Input('sports', 'n_clicks'), Input('sports', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.selectCategory(id)
    else:
        controllerObject.deselectCategory(id)
    return id


@app.callback(Output('hidden-div6', 'children'), inputs=[Input('science', 'n_clicks'), Input('science', 'id')])
def change_categories(n_clicks, id):
    if (n_clicks % 2) != 0:
        controllerObject.selectCategory(id)
        print('Science Button pressed')
    else:
        controllerObject.deselectCategory(id)
    return id





if __name__ == '__main__':
    app.run_server(debug=True)
