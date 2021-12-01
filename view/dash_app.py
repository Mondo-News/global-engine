import dash
from controller.controller import controllerObject
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Title of our awesome map'),
    html.Iframe(
        id='map',
        srcDoc=open('map.html', 'r').read(),
        width='100%',
        height='800'
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)