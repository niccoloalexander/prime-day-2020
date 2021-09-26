# Import Bootstrap from Dash
import os

import dash_bootstrap_components as dbc


app_name = os.getenv("DASH_APP_PATH", "/prime-day-2020-statistics")

# Navigation Bar fucntion
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Market Summary", href=f"{app_name}/market")),
            dbc.NavItem(dbc.NavLink("Customer Insights", href=f"{app_name}/customer")),
            # dbc.NavItem(dbc.NavLink("Ads Dashboard", href=f"{app_name}/ads-dash")),
        ],
        brand="Home",
        brand_href=f"{app_name}",
        sticky="top",
        color="light",
        dark=False,
        expand="lg",
    )
    return navbar
