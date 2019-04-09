# import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from .litmus_database import Litmus 

def plot_RGB(plotdata):
    data = []
    keys = plotdata.keys()
    for key in keys :
        for item in plotdata[key]['list']:
            if not item['case'] == 'giant':
                pointname = item['litmus']['name']
                if item['case'] == 'self' :
                    pointsize = 14
                    pointsymbol = 'square'
                elif item['case'] == 'supernova':
                    pointsize = 10
                    pointsymbol = 'diamond'
                else :
                    pointsize = 6
                    pointsymbol = 'circle'

                trace = go.Scatter3d(
                    x=[item['litmus']['rgb'][0]],
                    y=[item['litmus']['rgb'][1]],
                    z=[item['litmus']['rgb'][2]],
                    name = pointname,
                    mode='markers + text', 
                    text= pointname,      
                    marker=dict(
                        size = pointsize,
                        color= item['litmus']['hexa'],
                        opacity=1,
                        symbol=pointsymbol,
                    ),
                    hoverinfo='name',  
                    hoverlabel=dict(
                        bgcolor = '#d0d0d0',
                        bordercolor = '#808080',
                    ),
                    showlegend = False
                )
                data.append(trace)
    layout = go.Layout(
        height=500,
        width=500,
        margin=dict(l=0, r=0, b=30, t=30)
        # xaxis='R',
        # yaxis='G',
        # zaxis='Z'
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div