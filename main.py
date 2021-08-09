import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import geopandas as gpd
import pyproj
import numpy as np
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash

app = JupyterDash(__name__)

df = pd.read_csv('data.csv')
nb = 'shapefile\RAjasthan_admin_Dist_Boundary.shp'
map_df = gpd.read_file(nb)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

goals = list(df.columns)[1:-2]
graphs = []

reverse_indicators = ["Percentage of the children aged under 5 years who are stunted"] #Add names of reversed indicators here

for goal in goals:
    label_colour = "#007efc"
    colorscale = 'Reds'
    if(goal in reverse_indicators):
        colorscale += "_r"
    merged = map_df.set_index('DIST_NAME').join(df.set_index('DIST_NAME'))
    fig = px.choropleth(
            df, geojson=merged.geometry,
            hover_name="DIST_NAME",
            hover_data={
                'DIST_NAME': False,
                goal: True,
            },
            color=goal,
            color_continuous_scale=colorscale,
            locations="DIST_NAME",
            title=goal,
            )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    fig.add_trace(go.Scattergeo(lon=merged["Longitude"],
        lat=merged["Latitude"],
        text='<a style="text-decoration: none;" href="https://google.com">'+merged.index+'</a>',
        textposition="middle right",
        mode='text',
        textfont=dict(
        color='white',
        size=12,
    ), hoverinfo="skip",
        showlegend=False))
    fig.add_trace(go.Scattergeo(lon=merged["Longitude"],
        lat=merged["Latitude"],
        text=merged.index,
        textposition="middle right",
        mode='text',
        textfont=dict(
        color=label_colour,
        size=12,
    ), hoverinfo="skip",
        showlegend=False))
    fig.update_layout(
        autosize=False,
        height=720,
        width=1080)

    fig.update_layout(coloraxis_showscale=False)
    graphs.append(dcc.Graph(
        id=goal,
        figure=fig,
        config={
            'displaylogo': False
        }
    ))

app.layout = html.Div(children=graphs)

#-------------------------------#

app.run_server(debug=True)