# Dash components, html, and dash tables
from dash import dcc
from dash import html
from dash import dash_table

# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
import data

# Import data from data.py file
sales_df = data.sales_df
ads_df = data.ads_df 
sales_customer_aggs = data.sales_customer_aggs
ads_customer_aggs = data.ads_customer_aggs

prime_day_start = '2020-10-13'
prime_day_end = '2020-10-14'

# Market menu
marketMenu = html.Div(
    [
        html.Div(
            [
                html.Div(children="Marketplace", className="menu-title"),
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "18px",
                        "width": "210px",
                    },
                    id= "marketplace-dropdown",
                    options= [
                            {"label": mkt, "value": mkt}
                            for mkt in sales_df['Marketplace'].unique()
                    ],
                    value= 'United States',
                    clearable= False,
                ),
            ]
        ),
    ],
    className="menu-small",
)

# Customer menu
customerMenu = html.Div(
    [
        html.Div(
            [
                html.Div(children="Marketplace", className="menu-title"),
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "18px",
                        "width": "210px",
                    },
                    id= "marketplace-dropdown-2",
                    options= [
                            {"label": mkt, "value": mkt}
                            for mkt in sales_customer_aggs['Marketplace'].unique()
                    ],
                    value= 'United States',
                    clearable= False,
                ),
            ]
        ),
        html.Div(
            [
                html.Div(children="Customer", className="menu-title"),
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "18px",
                        "width": "210px",
                    },
                    id= "customer-dropdown",
                    options= [
                            {"label": customer, "value": customer}
                            for customer in [customer for customer in (sales_customer_aggs['Customer'].unique()) if customer in ads_customer_aggs['Customer'].unique()]
                    ],
                    value= [customer for customer in (sales_customer_aggs['Customer'].unique()) if customer in ads_customer_aggs['Customer'].unique()][5],
                    clearable= False,
                ),
            ],
        ),
    ],
    className="menu",
)

# Layout for Market Summary page
marketLayout = html.Div(
    [
        dbc.Row(dbc.Col(html.H3(children="Sales Stats")), className= 'section'),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="med-sales-dt-chart", config={"displayModeBar": False}), className= 'bigcard',
            ),
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="sales-chart", config={"displayModeBar": False}), className= 'bigcard',
            ),
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="orders-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card',
                ),
                dbc.Col(
                    dcc.Graph(id="quantity-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card-lpad',
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(dbc.Col(html.H3(children="Ad Stats")), className= 'section'),
        html.Div(
            [
                html.Div(
                            [
                                html.Div(children="Sponsored Type", className="menu-title"),
                                dcc.Dropdown(
                                    style={
                                        "text-align": "center",
                                        "font-size": "18px",
                                        "width": "210px",
                                    },
                                    id= "sponsored-type-dropdown",
                                    options= [
                                            {"label": stype, "value": stype}
                                            for stype in ads_df['Sponsored Type'].unique()
                                    ],
                                    value= 'All',
                                    clearable= False,
                                ),
                            ]
                ),
            ],
            className="menu-small",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="ctr-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card',
                ),
                dbc.Col(
                    dcc.Graph(id="cpc-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card-lpad',
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="roas-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card',
                ),
                dbc.Col(
                    dcc.Graph(id="acos-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card-lpad',
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="ad-revenue-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card',
                ),
                dbc.Col(
                    dcc.Graph(id="ad-spending-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                    className= 'card-lpad',
                ),
            ],
            no_gutters=True,
        ),
    ],
    className="app-page",
)

# Layout for Customer Summary Page 

customerLayout = html.Div(
    [
        dbc.Row(
            dbc.Col(html.H3(children="Sales Stats")), className= 'section'
        ),
        html.Div(
            [
                dcc.Dropdown(
                    style={
                        "text-align": "center",
                        "font-size": "18px",
                        "width": "210px",
                    },
                    id= "sales-var-dropdown",
                    options= [
                            {"label": var, "value": var}
                            for var in sales_customer_aggs.columns[3:]
                    ],
                    value= 'Sales',
                    clearable= False,
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="sales-dt-cust-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 12, "offset": 0},
                    className= 'bigcard',
                ),
            ],
            no_gutters=True,
        ),
        dbc.Row(dbc.Col(html.H3(children="Ads Stats")), className= 'section'),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(children="Variable A", className="menu-title"),
                        dcc.Dropdown(
                            style={
                                "text-align": "center",
                                "font-size": "18px",
                                "width": "210px",
                            },
                            id= "ad-var-a-dropdown",
                            options= [
                                    {"label": var, "value": var}
                                    for var in ads_customer_aggs.columns[4:]
                            ],
                            value= 'Ad Revenue',
                            clearable= False,
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(children="Sponsored Type", className="menu-title"),
                        dcc.Dropdown(
                            style={
                                "text-align": "center",
                                "font-size": "18px",
                                "width": "210px",
                            },
                            id= "sponsored-type-dropdown-2",
                            options= [
                                    {"label": stype, "value": stype}
                                    for stype in ads_customer_aggs['Sponsored Type'].unique()
                            ],
                            value= 'All',
                            clearable= True,
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Div(children="Variable B", className="menu-title"),
                        dcc.Dropdown(
                            style={
                                "text-align": "center",
                                "font-size": "18px",
                                "width": "210px",
                            },
                            id= "ad-var-b-dropdown",
                            options= [
                                    {"label": var, "value": var}
                                    for var in ads_customer_aggs.columns[4:]
                            ],
                            value= 'ACoS',
                            clearable= False,
                        ),
                    ]
                ),
            ],
            className="menu-large",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="ad-dt-cust-chart", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 12, "offset": 0},
                    className= 'bigcard',
                ),
            ],
            no_gutters=True,
        ),
    ]
)