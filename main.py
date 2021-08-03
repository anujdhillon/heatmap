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


goal = "Percentage of the children aged under 5 years who are stunted"
label_colour = "#007efc"


df = pd.read_csv('data.csv')
names = ["NA","Aspirant","Performer","Front Runner","Achiever"]
bins = [0,1,49.99,64.99,99.99,np.inf]
df['Category'] = pd.cut(df[goal],bins,labels=names)
nb = 'shapefile\RAjasthan_admin_Dist_Boundary.shp'
map_df = gpd.read_file(nb)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
merged = map_df.set_index('DIST_NAME').join(df.set_index('DIST_NAME'))
fig = px.choropleth(
        df, geojson=merged.geometry,
        hover_name="DIST_NAME",
        hover_data={
            'DIST_NAME': False,
            goal: True,
        },
        color=goal,
        color_continuous_scale='Reds',
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
#fig.add_scattergeo(lat=merged['Latitude'], lon=merged['Longitude'],text="DIST_NAME",showlegend=False)
fig.update_layout(coloraxis_showscale=False)
fig2 = px.choropleth(
        df, geojson=merged.geometry,
        hover_name="DIST_NAME",
        hover_data={
            'DIST_NAME': False,
            'Category': False,
            goal: True,
        },
        color="Category",
        color_discrete_map={'Achiever':'#00AEEF','Front Runner': '#00A084','Performer': '#FFC40C','Aspirant': '#DE1D45','NA': 'black'},
        locations="DIST_NAME",
        title=goal,
        )
fig2.update_geos(fitbounds="locations", visible=False)
fig2.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
fig2.update_layout(showlegend=False)
fig2.add_trace(go.Scattergeo(lon=merged["Longitude"],
    lat=merged["Latitude"],
    text='<a style="text-decoration: none;" href="https://google.com">'+merged.index+'</a>',
    textposition="middle right",
    mode='text',
    textfont=dict(
    color='white',
    size=12,
), hoverinfo="skip",
    showlegend=False))
#fig.add_scattergeo(lat=merged['Latitude'], lon=merged['Longitude'],text="DIST_NAME",showlegend=False)
fig2.add_trace(go.Scattergeo(lon=merged["Longitude"],
              lat=merged["Latitude"],
              text=merged.index,
              textposition="middle right",
               mode='text',
               textfont=dict(
            color=label_colour,
            size=12,
            
        ),
        hoverinfo="skip",
              showlegend=False))
fig2.update_layout(
    autosize=False,
    height=720,
    width=1080)
#fig.write_html("map_html.html") to save html
#fig.show() #to open in the browser

app = JupyterDash(__name__)
app.layout = html.Div(children=[    
    dcc.Graph(
        id='choropleth',
        figure=fig
    ),
    dcc.Graph(
        id='choropleth2',
        figure=fig2
    )
],style={'display':'flex'})

#-------------------------------#

app.run_server(debug=True)