# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


# Create a dash application
app = dash.Dash(__name__)

LaunchSite =spacex_df['Launch Site'].unique()
ddoptions = [{'label': 'All Sites', 'value': 'ALL'}]
for i in LaunchSite:
    ddoptions.append({'label': i, 'value': i})

min_value = spacex_df['Payload Mass (kg)'].min()
max_value = spacex_df['Payload Mass (kg)'].max()

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                html.Label("Select Launch Site:"),
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=ddoptions,
                                    value='',
                                    placeholder='Select Launch Site',
                                    style={'width':'80%','padding':'3px','font-size':'20px','text-align-last':'center'}
                                )
                                ]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                               
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,                                                
                                                value=[min_value, max_value]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))
def get_graph(salectedLS):
    if salectedLS == 'ALL':
        piedf=spacex_df.loc[spacex_df['class']==1]
        count_df=piedf.groupby(['Launch Site'])['class'].count().reset_index()
        pie_fig = px.pie(count_df, names='Launch Site', values='class', title='total successful launches count')
    else:
        piedf=spacex_df.loc[spacex_df['Launch Site']==salectedLS]
        count_df =piedf['class'].value_counts().reset_index()
        count_df['class'].replace(0,'Failure',inplace=True)
        count_df['class'].replace(1,'Success',inplace=True)
        pie_fig = px.pie(count_df, names='class', values='count', title='Success vs. Failed counts')
    return pie_fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def get_scatter_graph(salectedLS,slidervalue):
    if salectedLS == 'ALL':  
        scatterdf=spacex_df.loc[(spacex_df['Payload Mass (kg)'] <= slidervalue[1]) & (spacex_df['Payload Mass (kg)'] >= slidervalue[0])]
        scatter_fig = px.scatter(scatterdf, x="Payload Mass (kg)", y="class")
    else:
        scatdf=spacex_df.loc[spacex_df['Launch Site']==salectedLS]
        scatterdf=scatdf.loc[(scatdf['Payload Mass (kg)'] <= slidervalue[1]) & (scatdf['Payload Mass (kg)'] >= slidervalue[0])]
        scatter_fig = px.scatter(scatterdf, x="Payload Mass (kg)", y="class")
    return scatter_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
