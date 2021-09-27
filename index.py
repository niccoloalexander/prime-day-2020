# import dash-core, dash-html, dash io, bootstrap
import os

from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks
from navbar import Navbar
from layouts import (
    marketMenu,
    customerMenu,
    marketLayout,
    customerLayout,
    # adsLayout,
)
import callbacks

# Import app
from app import app

# Import server for deployment
from app import srv as server

import base64

image_filename = "assets/2020.jpg"
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app_name = os.getenv("DASH_APP_PATH", "/prime-day-2020-statistics")

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.Img(
                            src='data:image/png;base64,{}'.format(encoded_image.decode()), 
                            # height= '256px',
                            # width= '256px',
                            className= 'pic',
                        ),
                html.H2(children="A Visual Summary"),
            ]
        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])


# Menu callback, set and return
# Declair function  that connects other pages with content to container
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in [app_name, "{}/".format(app_name)]:
        return html.Div(
            [
                dcc.Markdown(
                    """
            ### The App
            This app was built by Niccolo Alexander Hamlin to explore how Amazon Prime Day affects customer sales and advertisting as detailed in the prompt below. 
            It was built using Plotly Dash, Dash Bootsrap Components, Pandas, and SQLite. All figures are generated with mock data.

            ### The Prompt
            "*Amazon Prime Day is an annual deal event exclusively for Prime members, delivering two days of epic deals on products on all kind of businesses and brands."*

            * What was the impact of Prime Day on Sales? 
            * Is advertising efficient during the event? 
            * What type of advertising worked best? 

            ### To Begin:
            Use the navigation bar at the top to open the market summary or customer insights dashboards.
        """
                )
            ],
            className="home",
        )
    elif pathname.endswith("/market"):
        return marketMenu, marketLayout
    elif pathname.endswith("/customer"):
        return customerMenu, customerLayout
    # elif pathname.endswith("/ads-dash"):
    #     return appMenu, menuSlider, playerMenu, adsLayout
    else:
        return "ERROR 404: Page not found!"


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(debug=True)
