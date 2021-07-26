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

df = pd.read_csv('data.csv')
criteria = [df['Goal 2 Score'].between(0, 33), df['Goal 2 Score'].between(34, 66), df['Goal 2 Score'].between(66, 100)]
names = ["Aspirant","Performer","Front Runner","Achiever"]
bins = [0,49.99,64.99,99.99,np.inf]
df['Category'] = pd.cut(df['Goal 2 Score'],bins,labels=names)
nb = 'shapefile\RAjasthan_admin_Dist_Boundary.shp'
map_df = gpd.read_file(nb)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
merged = map_df.set_index('DIST_NAME').join(df.set_index('DIST_NAME'))
fig = px.choropleth(merged, geojson=merged.geometry, locations=merged.index, color=df['Category'],color_discrete_map={'Achiever':'#00AEEF','Front Runner': '#00A084','Performer': '#FFC40C','Aspirant': '#DE1D45'})
fig.update_geos(fitbounds="locations", visible=False)
#fig.add_scattergeo(lat=merged['Latitude'], lon=merged['Longitude'],text="DIST_NAME",showlegend=False)
fig.add_trace(go.Scattergeo(lon=merged["Longitude"],
              lat=merged["Latitude"],
              text=merged.index,
              textposition="middle right",
               mode='text',
               textfont=dict(
            color='white',
            size=12,
        ),
              showlegend=False))
#fig.write_html("map_html.html") to save html
#fig.show() #to open in the browser

app = JupyterDash(__name__)
app.layout = html.Div([    
    dcc.Graph(
        id='choropleth',
        figure=fig
    )
])

#-------------------------------#

@app.callback(
    Output('choropleth', 'figure'),
    [Input('choropleth', 'clickData')])
def update_figure(clickData):    
    if clickData is not None:            
        location = clickData['points'][0]['location']
        print("You clicked",location)
        

app.run_server(mode='inline')