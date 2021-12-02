import dash
from controller.controller import controllerObject
from dash import html, dcc
from dash.dependencies import Input, Output

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
        html.H1('Mondo News', style={'font-size': '34pt', 'margin-bottom': '0px', 'margin-top': '5px', 'padding-bottom': '0px'}),
        html.P('Your visual global news platform',
               style={'color': '#968C83', 'font-size': '16pt', 'margin-top': '0px', 'padding-top': '0px'}),
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
        html.Button(id='button-technology',
                    children=['Technology'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='button-health',
                    children=['Health'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='button-science',
                    children=['Science'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='button-business',
                    children=['Business'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='button-sports',
                    children=['Sports'],
                    n_clicks=0,
                    style=white_button_style
                    )
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    html.Iframe(
        id='map',
        srcDoc=open('map.html', 'r').read(),
        width='100%',
        height='800'
    )

], style={'display': 'flex', 'flex-direction': 'column', 'font-family': 'Corbel'})


@app.callback(Output('button-technology', 'style'), [Input('button-technology', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('button-health', 'style'), [Input('button-health', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('button-science', 'style'), [Input('button-science', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('button-business', 'style'), [Input('button-business', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


@app.callback(Output('button-sports', 'style'), [Input('button-sports', 'n_clicks')])
def change_button_style(n_clicks):
    if (n_clicks % 2) != 0:
        return red_button_style
    else:
        return white_button_style


if __name__ == '__main__':
    app.run_server(debug=True)
