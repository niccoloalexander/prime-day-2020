# import dash IO and graph objects
from dash.dependencies import Input, Output

# Plotly graph objects to render graph plots
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Import dash html, bootstrap components, and tables for datatables
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

# Import app
from app import app

# Import custom data.py
import data

# Import data from data.py file
sales_dt_df = data.sales_dt_df
sales_df = data.sales_df
ads_df = data.ads_df 
sales_customer_aggs = data.sales_customer_aggs
ads_customer_aggs = data.ads_customer_aggs

from datetime import datetime, timedelta

prime_day_start = '2020-10-13'
prime_day_end = '2020-10-14'

@app.callback(
    [
        Output("sales-chart", "figure"),
        Output("orders-chart", "figure"),
        Output("quantity-chart", "figure"),
        # Output("sales-dt-chart", "figure"),
        Output("med-sales-dt-chart", "figure"),
    ],
    [
        Input("marketplace-dropdown", "value"),
    ],
)
def update_sales_stats(marketplace):

    mask = (
        (sales_df['Marketplace'] == marketplace)
    )
            
    filtered_data = sales_df.loc[mask, :]

    mask = (
        (sales_dt_df['Marketplace'] == marketplace)
    )
            
    filtered_dt_data = sales_dt_df.loc[mask, :]
    
    var = 'Median 2-Day Sales'

    chart1 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart1.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart1.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'prefix': '$'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart1.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_tickprefix = '$',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median 2-Day Orders'

    chart2 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart2.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart2.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart2.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median 2-Day Quantity'

    chart3 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart3.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart3.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart3.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

#     var = 'Total Sales'

#     chart4 = px.line(
#                         filtered_dt_data, 
#                         x= 'Date', y= var, 
#                         title= '''US Market {}'''.format(var), 
#                         template= 'none',
#                         markers= True,
# #                         hover_data= {variable: '{}'.format(':$.2f' if variable in dollar_cols else ':.2f')},
#                     )
    
#     chart4.update_traces(hovertemplate= None)
    
#     chart4.update_layout(
#         hovermode= 'x',
#         yaxis_tickprefix = '$',
# #         yaxis_tickformat = '.2f',
#         shapes=[
#             dict(
#                 type= 'rect',
#                 xref= 'x',
#                 yref= 'y',
#                 x0= datetime.strptime(prime_day_start, '%Y-%m-%d') - timedelta(0.2),
#                 y0= '0',
#                 x1= datetime.strptime(prime_day_end, '%Y-%m-%d') + timedelta(0.2),
#                 y1= filtered_dt_data[var].max() + filtered_dt_data[var].max() * .05,
# #                 fillcolor= 'lightgray',
#                 fillcolor= '#00AAE2',
#                 opacity= 0.2,
#                 line_width= 0,
#                 layer= 'below',
#             ),
#         ],
#     )
        
#     chart4.add_annotation(
#             x= datetime.strptime(prime_day_start, '%Y-%m-%d') + timedelta(0.5), 
#             y= filtered_dt_data[var].max() + filtered_dt_data[var].max() * .1,
#             text= '<b>Prime Day</b>',
#             showarrow= False,
#             font= {'family': 'Franklin Gothic'},
#     )

    var = 'Median Sales'

    chart5 = px.line(
                        filtered_dt_data, 
                        x= 'Date', y= var, 
                        title= '''US Market {}'''.format(var), 
                        template= 'none',
                        markers= True,
#                         hover_data= {variable: '{}'.format(':$.2f' if variable in dollar_cols else ':.2f')},
                    )
    
    chart5.update_traces(hovertemplate= None)
    
    chart5.update_layout(
        hovermode= 'x',
        yaxis_tickprefix = '$',
#         yaxis_tickformat = '.2f',
        shapes=[
            dict(
                type= 'rect',
                xref= 'x',
                yref= 'y',
                x0= datetime.strptime(prime_day_start, '%Y-%m-%d') - timedelta(0.2),
                y0= '0',
                x1= datetime.strptime(prime_day_end, '%Y-%m-%d') + timedelta(0.2),
                y1= filtered_dt_data[var].max() + filtered_dt_data[var].max() * .05,
#                 fillcolor= 'lightgray',
                fillcolor= '#00AAE2',
                opacity= 0.2,
                line_width= 0,
                layer= 'below',
            ),
        ],
    )
        
    chart5.add_annotation(
            x= datetime.strptime(prime_day_start, '%Y-%m-%d') + timedelta(0.5), 
            y= filtered_dt_data[var].max() + filtered_dt_data[var].max() * .1,
            text= '<b>Prime Day</b>',
            showarrow= False,
            font= {'family': 'Franklin Gothic'},
    )
    
    return chart1, chart2, chart3, chart5

@app.callback(
    [
        Output("ad-revenue-chart", "figure"),
        Output("ad-spending-chart", "figure"),
        Output("roas-chart", "figure"),
        Output("acos-chart", "figure"),
        Output("ctr-chart", "figure"),
        Output("cpc-chart", "figure"),
    ],
    [
        Input("marketplace-dropdown", "value"),
        Input("sponsored-type-dropdown", "value"),
    ],
)
def update_ad_stats(marketplace, stype):

    mask = (
        (ads_df['Marketplace'] == marketplace)
        & (ads_df['Sponsored Type'] == stype)
    )
            
    filtered_data = ads_df.loc[mask, :]
    
    var = 'Median 2-Day Ad Revenue'

    chart1 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart1.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart1.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'prefix': '$'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart1.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_tickprefix = '$',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median 2-Day Ad Spending'

    chart2 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart2.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart2.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'prefix': '$'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart2.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_tickprefix = '$',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median ROAS'

    chart3 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
    )

    chart3.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart3.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'suffix': '%'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart3.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_ticksuffix = '%',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median ACoS'

    chart4 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
    )

    chart4.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart4.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'suffix': '%'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    'decreasing': {'color': '#3D9970'},
                    'increasing': {'color': '#FF4136'},
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart4.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_ticksuffix = '%',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median CTR'

    chart5 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
    )

    chart5.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart5.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'suffix': '%'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart5.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_ticksuffix = '%',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    var = 'Median CPC'

    chart6 = make_subplots(
        rows=1, cols=2,
        column_widths= [0.7, 0.3],
        specs= [[{'type': 'bar'}, {'type': 'indicator'}]],
        # subplot_titles=("Plot 1", "Plot 2"),
    )

    chart6.add_trace(
        go.Bar(
            x= filtered_data['Period'], 
            y= filtered_data[var],
            marker= dict(color= ['#242C40', '#00AAE2']),
        ),
        row=1, col=1,
    )

    chart6.add_trace(
        go.Indicator(
            mode = 'number+delta',
            value = filtered_data[filtered_data['Period'] == 'Prime Day'][var].values[0],
            number = {'prefix': '$'},
            delta = {'position': 'top', 
                    'reference': filtered_data[filtered_data['Period'] == 'Non-Prime Day'][var].values[0],
                    'decreasing': {'color': '#3D9970'},
                    'increasing': {'color': '#FF4136'},
                    },
            domain = {'x': [0, 1], 'y': [0, 1]},
            title= 'Prime Day',
        ),
        row=1, col=2,
    )

    chart6.update_layout(
        title={'text': var},
        template= 'none',
        hovermode= 'x',
        yaxis_tickprefix = '$',
        margin= dict(
            l= 80,
            r= 80,
            b= 50,
            t= 80,
        ),
    )

    return chart1, chart2, chart3, chart4, chart5, chart6 

@app.callback(
    [
        Output("sales-dt-cust-chart", "figure"),
        Output("ad-dt-cust-chart", "figure"),
    ],
    [
        Input("marketplace-dropdown-2", "value"),
        Input("customer-dropdown", "value"),
        Input("sponsored-type-dropdown-2", "value"),
    ],
)
def update_cust_stats(marketplace, customer, stype):

    mask = (
        (sales_customer_aggs['Marketplace'] == marketplace)
        & (sales_customer_aggs['Customer'] == customer)
    )
            
    filtered_data = sales_customer_aggs.loc[mask, :]

    if stype != None:

        mask = (
            (ads_customer_aggs['Marketplace'] == marketplace)
            & (ads_customer_aggs['Customer'] == customer)
            & (ads_customer_aggs['Sponsored Type'] == stype)
        )

    else: 

        mask = (
            (ads_customer_aggs['Marketplace'] == marketplace)
            & (ads_customer_aggs['Customer'] == customer)
            & (ads_customer_aggs['Sponsored Type'] != 'All')
        )
            
    filtered_ad_data = ads_customer_aggs.loc[mask, :]
    
    var = 'Sales'
    dollar_cols = ['Sales', 'Average Price', 'Median Price']

    chart1 = px.line(
                        filtered_data, 
                        x= 'Date', y= var, 
                        title= '''Customer's {}'''.format(var),
                        template= 'none',
                        markers= True,
                    )
        
    chart1.update_layout(
        hovermode= 'x',
        yaxis_tickprefix = '{}'.format('$' if var in dollar_cols else ''),
#         yaxis_tickformat = '.2f',
        shapes=[
            dict(
                type= 'rect',
                xref= 'x',
                yref= 'y',
                x0= datetime.strptime(prime_day_start, '%Y-%m-%d') - timedelta(0.2),
                y0= '0',
                x1= datetime.strptime(prime_day_end, '%Y-%m-%d') + timedelta(0.2),
                y1= filtered_data[var].max() + filtered_data[var].max() * .05,
#                 fillcolor= 'lightgray',
                fillcolor= '#00AAE2',
                opacity= 0.2,
                line_width= 0,
                layer= 'below',
            ),
        ],
    )
        
    chart1.add_annotation(
            x= datetime.strptime(prime_day_start, '%Y-%m-%d') + timedelta(0.5), 
            y= filtered_data[var].max() + filtered_data[var].max() * .1,
            text= '<b>Prime Day</b>',
            showarrow= False,
            font= {'family': 'Franklin Gothic'},
    )

    var1 = 'Ad Revenue'
    var2 = 'ACoS'

    chart2 = make_subplots(specs=[[{'secondary_y': True}]])

    
    for stype in filtered_ad_data['Sponsored Type'].unique():
        
        chart2.add_trace(go.Bar(x= filtered_ad_data[filtered_ad_data['Sponsored Type'] == stype]['Date'], 
                                       y= filtered_ad_data[filtered_ad_data['Sponsored Type'] == stype][var1],
                                       name= '{}, {}'.format(var1, stype),
                                      )
                               )
    
    for stype in filtered_ad_data['Sponsored Type'].unique():
        
        chart2.add_trace(
            go.Scatter(x= filtered_ad_data[filtered_ad_data['Sponsored Type'] == stype]['Date'], 
                            y= filtered_ad_data[filtered_ad_data['Sponsored Type'] == stype][var2], 
                            name= '{}, {}'.format(var2, stype),
                            yaxis= 'y2',
                            mode= 'lines+markers',
            )      
        )
        
    chart2.update_yaxes(rangemode= 'tozero',
#                                ticksuffix= '%'
                              )
        
    chart2.update_layout(
        template= 'none',
        hovermode= 'x',
        yaxis_tickprefix = '$',
#         yaxis_tickformat = '.2f',
        yaxis2= dict(
#             tickformat= '%',
            ticksuffix= '%',
            title= 'ACoS'
        ),
        title="Ad Revenue and ACoS",
        xaxis_title="Date",
        yaxis_title="Ad Revenue",
        legend= dict(
            title= 'Variable, Sponsored Type'
        ),
        shapes= [
            dict(
                type= 'rect',
                xref= 'x',
                yref= 'y',
                x0= datetime.strptime(prime_day_start, '%Y-%m-%d') - timedelta(0.5),
                y0= '0',
                x1= datetime.strptime(prime_day_end, '%Y-%m-%d') + timedelta(0.5),
                y1= filtered_ad_data[var1].max() + filtered_ad_data[var1].max() * .05,
#                 fillcolor= 'lightgray',
                fillcolor= '#00AAE2',
                opacity= 0.2,
                line_width= 0,
                layer= 'below',
            ),
        ],
    )
        
    chart2.add_annotation(
        x= datetime.strptime(prime_day_start, '%Y-%m-%d') + timedelta(0.5), 
        y= filtered_ad_data[var1].max() + filtered_ad_data[var1].max() * .1,
        text= '<b>Prime Day</b>',
        showarrow= False,
        font= {'family': 'Franklin Gothic'},
    )

    return chart1, chart2 