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
names = ["NA","Aspirant","Performer","Front Runner","Achiever"]
bins = [0,1,49.99,64.99,99.99,np.inf]
nb = 'shapefile\RAjasthan_admin_Dist_Boundary.shp'
map_df = gpd.read_file(nb)
goals = df.columns[1:10]
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
merged = map_df.set_index('DIST_NAME').join(df.set_index('DIST_NAME'))
# fig = px.choropleth(merged, geojson=merged.geometry, locations=merged.index, color=pd.cut(df['G'],bins,labels=names),color_discrete_map={'Achiever':'#00AEEF','Front Runner': '#00A084','Performer': '#FFC40C','Aspirant': '#DE1D45'}, hover_name=merged.index)
# fig.update_geos(fitbounds="locations", visible=False)
#fig.add_scattergeo(lat=merged['Latitude'], lon=merged['Longitude'],text="DIST_NAME",showlegend=False)
#fig.write_html("map_html.html") to save html
#fig.show() #to open in the browser

app =dash.Dash(__name__)
app.layout = html.Div([
    html.P("Goal:"),
    dcc.RadioItems(
        id='goal', 
        options=[{'value': x, 'label': x} 
                 for x in goals],
        value=goals[0],
        labelStyle={'display': 'block'}
    ),    
    dcc.Graph(
        id='choropleth',
    )
])

#-------------------------------#

# @app.callback(
#     Output('choropleth', 'figure'),
#     [Input('choropleth', 'clickData')])
# def update_figure(clickData):    
#     if clickData is not None:            
#         location = clickData['points'][0]['location']
#         print("You clicked",location)
        
@app.callback(
    Output("choropleth", "figure"), 
    [Input("goal", "value")])
def display_choropleth(goal):
    df['Category'] = pd.cut(df[goal],bins,labels=names)
    fig = px.choropleth(
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
        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell"
    )
)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
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
    return fig

app.run_server(debug=True)