import dash
from controller.controller import controllerObject
from dash import html, dcc
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

white_button_style = {'background-color': 'white',
                      'color': 'black',
                      'height': '50px',
                      'width': '100px',
                      'margin-top': '50px',
                      'margin-left': '50px'}

red_button_style = {'background-color': 'red',
                    'color': 'white',
                    'height': '50px',
                    'width': '100px',
                    'margin-top': '50px',
                    'margin-left': '50px'}

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Mondo News', style={'font-size': '34pt', 'margin-bottom': '0px', 'padding-bottom': '0px'}),
        html.P('Your visual global news platform',
               style={'color': '#968C83', 'font-size': '16pt', 'margin-top': '0px', 'padding-top': '0px'}),
    ], style={'text-align': 'center'}),

    html.Div(children=[
        dcc.Input(value='Search...', type='text', style={'width': '300px', 'height': '25px', 'margin-bottom': '20px'}),
        html.Button(id='button',
                    children=['click'],
                    n_clicks=0,
                    style=white_button_style
                    ),
        html.Button(id='button',
                            children=['click'],
                            n_clicks=0,
                            style=white_button_style
                            ),
        html.Button(id='button',
                            children=['click'],
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


@app.callback(Output('button', 'style'), [Input('button', 'n_clicks')])
def change_button_style(n_clicks):
    if n_clicks > 0:
        return red_button_style
    else:
        return white_button_style


if __name__ == '__main__':
    app.run_server(debug=True)
