import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime as dt
import datetime as dt
import json
import dash_table_experiments as dtt

df = pd.read_csv('df_main.csv')
df1 = pd.DataFrame(df.groupby('Subscription_Date')[['Revenue','Profit']].sum()).reset_index()
#df1_2 = df.groupby(['Product type','Year']).agg({'Profit': ['sum','count']}).reset_index()

app = dash.Dash()

signature = '''
Created by [Bamby Gassama](https://www.bginsights.co/)
'''

notes = '''
 - **Best Customers (111):** Bought most recently and most often and spend the most
 **Action:** No price incentives, new products, and loyalty programs
 - **Loyal Customers (X1X):** Buy most frequently
**Action:** Use R and M to further segment
 - **Big spenders (XX1):** Spend the most
**Action:** Market your most expensive products
 - **Almost Lost (311):** Haven't purchased for some time, but purchased frequently and spend the most
**Action:** Aggressive price incentives
 - **Lost Customers (411):** Haven't purchased for some time, but purchased frequently and spend the most
**Action:** Aggressive price incentives
 - **Lost Cheap Customers (444):** Last purchased long ago, purchased few and spent little
**Action:** Don't spend too much trying to re-acquire
'''




countryoptions = []
for country in df['Country'].unique():
    countryoptions.append({'label':str(country),'value':country})

app.layout = html.Div([
                html.Div([
                    html.H1('Urban Sport Club Dashboard'),
                    dcc.Dropdown(id='country-picker',options=countryoptions,value='All'),
                    dcc.DatePickerRange(
                        id="my-date-picker-range",
                        start_date=dt.datetime(2015,2,2),
                        end_date=dt.datetime(2016,4,1),
                        calendar_orientation='vertical',
),

                ],style={"textAlign":"center"}),
#####

                html.Div([
                    html.H2('General'),
                    html.H4(id='rev',style={'textAlign':'center'})

                ]),


                html.Div([
                    dcc.Graph(id='sales_revenue_profit')

                ],style={'width':1200,'display':'inline-block','paddingLeft':100}),
                html.Div([
                    dcc.Graph(id='sales_revenue_profit_product')

                ],style={'width':700,'display':'inline-block'}),

                html.Div([
                    dcc.Graph(id='sales_revenue_sales_product')

                ],style={'width':700,'display':'inline-block'}),

#second row

                html.Div([
                    html.H2('Marketing'),
                    html.H4(id='mar',style={'textAlign':'center'})
                ]),

                html.Div([
                    dcc.Graph(id='hhhh')
                ],style={'width':450,'display':'inline-block'}),
                html.Div([
                    dcc.Graph(id='marketing_revenue_channels')

                    ],style={'width':450,'display':'inline-block'}),
                    html.Div([
                    dcc.Graph(id='marketing_channel_profit')

                    ],style={'width':450,'display':'inline-block'}),
#third row

                html.Div([
                    html.H2('Customers')
                ]),

                html.Div([
                    dcc.Graph(id='heatmapp')
                ],style={'width':700,'display':'inline-block'}),
                html.Div([
                    dcc.Graph(id='linechart')

                    ],style={'width':700,'display':'inline-block'}),
                    html.Div([
                    dcc.Graph(id='customer_analysis2',style={'height':700}),
                    dcc.Markdown(children=notes)


                    ],style={'width':1400,'display':'inline-block'}),

                    html.Div([
                        dcc.Graph(id='customer_analysis')

                    ],style={'width':1400,'display':'inline-block'}),

            html.Div([
                dcc.Markdown(children=signature)],
                style={'textAlign':'right','paddingRight':10})

             ], style={'margin':10})
#sig

@app.callback(Output('sales_revenue_profit_product','figure'),
              [Input('country-picker','value')])
def update_figure(country):
    df1_2 = df[df['Country']==country].groupby(['Product_Type','Year']).agg({'Profit': ['sum','mean']}).reset_index()
    traces = []
    for product in df1_2['Product_Type'].unique():
        newdf1_2 = df1_2[df1_2['Product_Type']==product]
        traces.append(go.Bar(
                x= newdf1_2['Year'],
                y= newdf1_2['Profit']['mean'],
                name = product

            ))

    return {
        'data':traces,
        'layout':go.Layout(
            barmode='relative',
            title = 'Average Profit by Product',
            xaxis = {'title':'Year'},

            yaxis = {'title':'Avg.Profit'}

        )
    }



####

@app.callback(Output('sales_revenue_sales_product','figure'),
              [Input('country-picker','value')])
def update_figure(country):
    df1_2 = df[df['Country']==country].groupby(['Product_Type','Year']).agg({'Profit': ['sum','count']}).reset_index()
    traces = []
    for product in df1_2['Product_Type'].unique():
            newdf1_2 = df1_2[df1_2['Product_Type']==product]
            traces.append(go.Bar(
                x= newdf1_2['Year'],
                y= newdf1_2['Profit']['count'],
                name = product

            ))

    return {
        'data':traces,
        'layout':go.Layout(
            barmode='group',
            title = 'Total Subscriptions Sold',
            xaxis = {'title':'Year'},
            yaxis = {'title':'Sum'}

        )
    }

####

@app.callback(Output('marketing_revenue_channels','figure'),
              [Input('country-picker','value')])
def update_figure(country):
    df1_3 = df[df['Country']==country].groupby(['Marketing_Channel','Product_Type']).agg({'Revenue': ['sum','count']}).reset_index()
    traces = []
    for product in df1_3['Product_Type'].unique():
            newdf1_3 = df1_3[df1_3['Product_Type']==product]
            traces.append(go.Bar(
                x= newdf1_3['Revenue']['sum'],
                y= newdf1_3['Marketing_Channel'],
                orientation='h',
                name = product

            ))

    return {
        'data':traces,
        'layout':go.Layout(
            barmode='stack',
            title = 'Revenue by Marketing Channel and Product Type',
            xaxis = {'title':'Revenue'},

            yaxis = {'title':'Product Type'}

        )
    }

######

@app.callback(Output('hhhh','figure'),
              [Input('country-picker','value')])
def update_figure(country):
    df1_3 = df[df['Country']==country].groupby(['Marketing_Channel']).agg({'Revenue': ['sum','count']}).reset_index()
    traces = []
    traces.append(go.Pie(
        values= df1_3['Revenue']['sum'],
        labels= df1_3['Marketing_Channel'],
        hole=.4,
        type='pie'

            ))

    return {
        'data':traces,
        'layout':go.Layout(
            barmode='stack',
            title = 'Revenue % by Marketing Channel '

        )
    }

####
@app.callback(Output('sales_revenue_profit','figure'),
              [Input('country-picker','value')])
def update_figure(country):

    df1_4 = df[(df['Country']==country)].groupby('Subscription_Date')[['Revenue','Profit','Cost']].sum().reset_index()
    df1ee =df[(df['Country']==country)].groupby('Subscription_Date')[['Cost']].count().reset_index()
    traces = []
    traces.append(go.Scatter(
        x= df1_4['Subscription_Date'],
        y= df1_4['Revenue'],
        mode='lines',
       name = 'Revenue'

            ))
    traces.append(go.Scatter(
        x= df1_4['Subscription_Date'],
        y= df1_4['Profit'],
        mode='lines',
        name ='Profit'
                ))
    traces.append(go.Scatter(
            x= df1_4['Subscription_Date'],
            y= df1_4['Cost'],
            mode='lines',
            name ='Cost'
                    ))
    traces.append(go.Scatter(
        x= df1ee['Subscription_Date'],
        y= df1ee['Cost'],
        mode='lines',
        name ='Units'
                        ))

    return {
        'data':traces,
        'layout':go.Layout(

            title = 'Revenue, Profit, Cost evolution',
            xaxis = {'title':'Subscription Date'},
            yaxis = {'title':'Total'}

        )
    }

######
@app.callback(Output('marketing_channel_profit','figure'),
              [Input('country-picker','value')])
def update_figure(country):
    df1_5 = df[df['Country']==country].groupby(['Marketing_Channel'])[['Profit']].sum().reset_index()
    traces = []
    traces.append(go.Bar(
        x= df1_5['Marketing_Channel'],
        y= df1_5['Profit']
            ))


    return {
        'data':traces,
        'layout':go.Layout(

            title = 'Profit by marketing Channel',
            xaxis = {'title':'Channel'},

            yaxis = {'title':'Sum. Profit'}


        )
    }
#####
@app.callback(Output('heatmapp','figure'),
              [Input('country-picker','value')])
def update_heatmap(country):
    newtablename  = pd.read_csv('cohorts.csv').groupby(['Acquisition_Date_2','Subscription_Date_2','Country']).sum().xs(country,level='Country')
    # reindex the DataFrame
    newtablename.reset_index(inplace=True)
    newtablename.set_index(['Acquisition_Date_2', 'CohortPeriod'], inplace=True)
    # create a Series holding the total size of each CohortGroup
    cohort_group_size = newtablename['TotalUsers'].groupby(['Acquisition_Date_2']).first()
    newtablename['TotalUsers'].unstack(0)
    newtablename  = newtablename['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1).T.multiply(100).round(0)
    return({'data':[go.Heatmap(z= newtablename.values.tolist(),
                   x=newtablename.columns,
                   y=newtablename.index
                   )],
            'layout':go.Layout(
            title='Retention Rate heatmap in {}'.format(country),
            xaxis = {'title':'Periods'},

            yaxis = {'title':'Group'}
)

    })

######

@app.callback(Output('linechart','figure'),
              [Input('country-picker','value')])
def update_heatmap(country):
        """
        Creates an country specific retention line plot: average retention rate troughtout periods.

        """
        newtablename  = pd.read_csv('cohorts.csv').groupby(['Acquisition_Date_2','Subscription_Date_2','Country']).sum().xs(country,level='Country')
        # reindex the DataFrame
        newtablename.reset_index(inplace=True)
        newtablename.set_index(['Acquisition_Date_2', 'CohortPeriod'], inplace=True)
        # create a Series holding the total size of each CohortGroup
        cohort_group_size = newtablename['TotalUsers'].groupby(['Acquisition_Date_2']).first()
        newtablename['TotalUsers'].unstack(0)
        newtablename  = newtablename['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1).T
        aa = pd.DataFrame(newtablename.mean()).multiply(100).reset_index()

        #plot creation
        return({'data':[go.Scatter(x=aa.iloc[:,0],
                                   y=aa.iloc[:,1],

                   )],
            'layout':go.Layout(
                title='Average Retention Rate heatmap in {}'.format(country),
                xaxis = {'title':'Periods'},

                yaxis = {'title':'Retention Rate in %'})


    })

####
@app.callback(Output('customer_analysis','figure'),
              [Input('country-picker','value')])
def update_bubble(country):
        traces=[]
        """
        Creates an country specific retention line plot: average retention rate troughtout periods.

        """
        dfseg = pd.read_csv('segmentation.csv').set_index(['Customer_ID','Country'])
        dfsegnew = dfseg.xs(country,level='Country')

        for score in dfsegnew['RFMScore'].unique():
            newseg = dfsegnew[dfsegnew['RFMScore']==score]

            traces.append(go.Scatter(
                x= newseg['recency'],
                y= newseg['frequency'],
                mode='markers',
                name = score


            ))


        #plot creation
        return({'data':traces,
            'layout':go.Layout(
            title='Customer Segmentation in {}'.format(country),
            hovermode='closest',
            xaxis = {'title':'Recency in days'},
            yaxis = {'title':'Frequency'})


    })

###

####
@app.callback(Output('customer_analysis2','figure'),
              [Input('country-picker','value')])
def update_bubble(country):
        traces=[]
        """
        Creates an country specific retention line plot: average retention rate troughtout periods.

        """
        dfseg = pd.read_csv('segmented_rfm2.csv').set_index(['Customer_ID','Country'])
        dfsegnew = dfseg.xs(country,level='Country')

        for score in dfsegnew['Category'].unique():
            newseg = dfsegnew[dfsegnew['Category']==score].reset_index()
            traces.append(go.Scatter(
                x = newseg['recency'],
                y = newseg['frequency'],
                marker=dict(
                    size=15,
                    opacity=.7

                ),

                mode ='markers',
                text = newseg['Customer_ID'],
                name = score
            ))

        #plot creation
        return({'data':traces,
            'layout':go.Layout(title='Customer Segmentation in {}'.format(country),
            hovermode='closest',
            xaxis = {'title':'Recency in days'},
            yaxis = {'title':'Frequency'})

    })


@app.callback(Output('rev','children'),
              [Input('country-picker','value')])
def update_revenue_total(country):
    return '{} // Total Revenue: € '.format(country)+str(round(df[df['Country']==country]['Revenue'].sum()))+'       |      '+ 'Unit Sold: '+str(round(df[df['Country']==country]['Revenue'].count()))+ '        |       '+ 'Total Profit: € '+str(round(df[df['Country']==country]['Profit'].sum()))+ '        |       '+ 'CPS: € ' +str(round(df[df['Country']==country]['Cost'].sum()/df[df['Country']==country]['Cost'].count()))

###

@app.callback(Output('mar','children'),
              [Input('country-picker','value')])
def update_revenue_total(country):
    return '{} // CPS Channel 1: € '.format(country)+str(round(df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 1')]['Cost'].sum()/df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 1')]['Cost'].count()))+'       |      '+ 'Channel 2: € '+str(round(df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 2')]['Cost'].sum()/df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 2')]['Cost'].count()))+'       |      '+ 'Channel 3: € '+str(round(df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 3')]['Cost'].sum()/df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 3')]['Cost'].count()))+'       |      '+ 'Channel 4: € '+str(round(df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 4')]['Cost'].sum()/df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 4')]['Cost'].count()))+'       |      '+ 'Channel 5: € '+str(round(df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 5')]['Cost'].sum()/df[(df['Country']==country)&(df['Marketing_Channel']=='Channel 5')]['Cost'].count()))


#
# @app.callback(
#     Output('hover-data', 'children'),
#     [Input('customer_analysis2', 'selectedData')])
# def callback_image(selectedData):
#     json.dumps(selectedData, indent=2)
#     client= selectedData['points'][0]['text']
#     return 'You have selected the clients: '+ client



# @app.callback(Output('table', 'figure'),
#              [Input('country-picker','value')])
# def update_table(country):
#     dfseg = pd.read_csv('segmented_rfm2.csv').set_index(['Customer_ID','Country'])
#     dff = dfseg.xs(country,level='Country').head(10)
#     dfsegnew = ff.create_table(dff)
#     return dfsegnew


app.css.append_css({'external_url': 'https://codepen.io/iambamby/pen/NzNaPJ.css'})
if __name__ == '__main__':
    app.run_server()
