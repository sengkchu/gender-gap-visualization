import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import os
from random import randint



#Application object
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)
app.title ='Gender Gap Visualization Tool'



#CSS and Javascript
external_css = ["https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})
    
#Load in data:
data_sf = pd.read_csv('cleaned_sf.csv')
data_nb = pd.read_csv('cleaned_nb.csv')
job_categories = data_sf['Job_Group'].value_counts().index


    
#App Layouts
app.layout = html.Div(
  className='container-fluid',
  children=[
                              
    html.Div(className='row', 
             children=[
    
    #Plot dashboard                          
    html.Div(className='col-lg-2 p-3 mb-2 bg-light text-dark', 
             children=[
                     html.Div(dcc.Markdown('### Gender Gap Visualization Tool')),                     
                     html.Div(dcc.Markdown('''---''')),
                     html.Div(dcc.Markdown('''Based on the dataset on found [here](https://transparentcalifornia.com/).''')),
                     html.Div(dcc.Markdown('''For a full analysis of this dataset click [here](https://codingdisciple.com/sf-gender-gap.html).''')),
                     html.Div(dcc.Markdown('''---''')),                    
                     html.Div(className='',
                              children=[html.B('Select Job Category:'),
                     dcc.Dropdown(
                             id='input1',
                             options=[{'label': i, 'value': i} for i in job_categories],
                             value='Police'
                             )]
                     ),

                     html.Div(dcc.Markdown('''---''')),
                     
                     
                     html.Div(className='',
                              children=[html.B('Select Job Status:'),
                     dcc.RadioItems(
                             inputStyle={'display':'inline-block', 'margin-right':'5px'},
                             labelStyle={'display':'inline-block', 'margin-right':'15px'},
                             id='input2',
                             options=[
                                     {'label': 'Full Time', 'value': 'FT'},
                                     {'label': 'Part Time', 'value': 'PT'}
                                     ],
                             value='FT'
                             )]
                     ),
                     
                     html.Div(dcc.Markdown('''---''')),
                      
                     html.Div(className='',
                              children=[html.B('Select Pay:'), 
                     dcc.Checklist(
                             inputStyle={'display':'inline-block', 'margin-right':'5px'},
                             labelStyle={'display':'inline-block', 'margin-right':'100px'},                             
                             id='input3',
                             options=[
                                     {'label': 'Base Pay', 'value': 'BasePay'},
                                     {'label': 'Overtime Pay', 'value': 'OvertimePay'},
                                     {'label': 'Benefits', 'value': 'Benefits'},
                                     {'label': 'Other Pay', 'value': 'OtherPay'}                                    
                                     ],
                             values=['BasePay', 'OvertimePay', 'Benefits', 'OtherPay']
                             )]
                     ),
                     
                     html.Div(dcc.Markdown('''---''')),                     
#                     html.Div(dcc.Markdown('''© 2018 Seng Chu · Powered by [Dash, Plotly](https://github.com/plotly/dash), [Bootstrap](https://getbootstrap.com/)''')),                    
                     
            ]),
    
    #Plot elements     
    html.Div(className='col-lg-10 p-3 mb-2 bg-white text-dark',
             children=[                     
                     html.Div(
                             className='row',
                             children=[html.Div(dcc.Graph(id='output_sf_1'), className='col-lg-6'),
                                       html.Div(dcc.Graph(id='output_nb_1'), className='col-lg-6')]
                             ),
                     
                     html.Div(
                             className='row',
                             children=[html.Div(dcc.Graph(id='output_sf_2'), className='col-lg-3'),
                                       html.Div(dcc.Graph(id='output_sf_3'), className='col-lg-3'),
                                       html.Div(dcc.Graph(id='output_nb_2'), className='col-lg-3'),
                                       html.Div(dcc.Graph(id='output_nb_3'), className='col-lg-3')]
                             ),                        

             ]),
                   
])])    
    
    
#callbacks
@app.callback(
    Output(component_id='output_sf_1', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_sf_1(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_sf[data_sf['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    trace1 = go.Histogram(name = 'Male', x=male_group['temp_total'], opacity=0.7, histnorm='probability', marker={'color':'#9999ff'}, hoverinfo="x+y+name", hoverlabel={'bgcolor':'#000000'})
    trace2 = go.Histogram(name = 'Female', x=female_group['temp_total'],opacity=0.7, histnorm='probability', marker={'color':'#ff9999'}, hoverinfo="x+y+name", hoverlabel={'bgcolor':'#000000'})
    return {
            'data':[trace1, trace2],
            'layout': {
                'xaxis': {'title':'Yearly Income'},
                'yaxis': {'title':'Normalized Frequency'},
                'title': 'San Francisco Pay Distribution'
            }
        } 
            
@app.callback(
    Output(component_id='output_sf_2', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_sf_2(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_sf[data_sf['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    male_error = 1.96*male_group['temp_total'].std()/np.sqrt(male_group['temp_total'].shape[0])    
    female_error = 1.96*female_group['temp_total'].std()/np.sqrt(female_group['temp_total'].shape[0])
        
    trace1 = go.Bar(
            name = 'Male',
            x=[' '], 
            y=[male_group['temp_total'].mean()],
            error_y=dict(
                    type='data',
                    array=[male_error],
                    visible=True 
            ),
            marker={'color':['#9999ff']}, 
            hoverinfo="y+name",
            hoverlabel={'bgcolor':'#000000'}
    )                         
    trace2 = go.Bar(
            name = 'Female',
            x=[' '], 
            y=[female_group['temp_total'].mean()],
            error_y=dict(
                    type='data',
                    array=[female_error],
                    visible=True 
            ),
            marker={'color':['#ff9999']}, 
            hoverinfo="y+name",
            hoverlabel={'bgcolor':'#000000'}
    )
                
    return {
            'data':[trace1, trace2],
            'layout': {
                'showlegend':False,
                'title': 'San Francisco Average Yearly Pay'
            }
        }
            
@app.callback(
    Output(component_id='output_sf_3', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_sf_3(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_sf[data_sf['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    plot = go.Pie(
            labels = ['Male', 'Female'],
            values = [male_group.shape[0], female_group.shape[0]],
            marker={'colors':['#9999ff', '#ff9999']},
            textfont=dict(size=20),                 
            hoverinfo="label+value",
            hoverlabel={'bgcolor':'#000000'}
            )
    return {
            'data':[plot],
            'layout': {
                'title': 'San Francisco Gender Representation'
            }
        }  
@app.callback(
    Output(component_id='output_nb_1', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_nb_1(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_nb[data_nb['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    trace1 = go.Histogram(name = 'Male', x=male_group['temp_total'], opacity=0.7, histnorm='probability', marker={'color':'#9999ff'}, hoverinfo="x+y+name", hoverlabel={'bgcolor':'#000000'})
    trace2 = go.Histogram(name = 'Female', x=female_group['temp_total'],opacity=0.7, histnorm='probability', marker={'color':'#ff9999'}, hoverinfo="x+y+name", hoverlabel={'bgcolor':'#000000'})
    return {
            'data':[trace1, trace2],
            'layout': {
                'xaxis': {'title':'Yearly Income'},
                'yaxis': {'title':'Normalized Frequency'},
                'title': 'Newport Beach Pay Distribution'
            }
        } 
            
@app.callback(
    Output(component_id='output_nb_2', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_nb_2(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_nb[data_nb['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    male_error = 1.96*male_group['temp_total'].std()/np.sqrt(male_group['temp_total'].shape[0])    
    female_error = 1.96*female_group['temp_total'].std()/np.sqrt(female_group['temp_total'].shape[0])
        
    trace1 = go.Bar(
            name = 'Male',
            x=[' '], 
            y=[male_group['temp_total'].mean()],
            error_y=dict(
                    type='data',
                    array=[male_error],
                    visible=True 
            ),
            marker={'color':['#9999ff']}, 
            hoverinfo="y+name",
            hoverlabel={'bgcolor':'#000000'}
    )                         
    trace2 = go.Bar(
            name = 'Female',
            x=[' '], 
            y=[female_group['temp_total'].mean()],
            error_y=dict(
                    type='data',
                    array=[female_error],
                    visible=True 
            ),
            marker={'color':['#ff9999']}, 
            hoverinfo="y+name",
            hoverlabel={'bgcolor':'#000000'}
    )
                
    return {
            'data':[trace1, trace2],
            'layout': {
                'showlegend':False,
                'title': 'Newport Beach Average Yearly Pay'
            }
        }
            
@app.callback(
    Output(component_id='output_nb_3', component_property='figure'),
    [Input(component_id='input1', component_property='value'),
     Input(component_id='input2', component_property='value'),
     Input(component_id='input3', component_property='values')]
)
def update_nb_3(input_value1, input_value2, input_value3):
    #Filter data based on inputs
    filter_group = data_nb[data_nb['Job_Group'] == input_value1]
    filter_status = filter_group[filter_group['Status'] == input_value2]
    filter_pay = filter_status.copy()
    filter_pay['temp_total'] = 0
    for pay in input_value3:
        filter_pay['temp_total'] += filter_pay[pay]
    
    male_group = filter_pay[filter_pay['Gender'] == 'male']
    female_group = filter_pay[filter_pay['Gender'] == 'female']
    
    plot = go.Pie(
            labels = ['Male', 'Female'],
            values = [male_group.shape[0], female_group.shape[0]],
            marker={'colors':['#9999ff', '#ff9999']},
            textfont=dict(size=20),                  
            hoverinfo="label+value",
            hoverlabel={'bgcolor':'#000000'}
            )
    return {
            'data':[plot],
            'layout': {
                'title': 'Newport Beach Gender Representation'
            }
        }  
        
if __name__ == '__main__':
	app.server.run(debug=True, threaded=True)