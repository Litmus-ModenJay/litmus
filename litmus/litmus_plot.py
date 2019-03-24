# import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot

def plot_RGB(plotdata):

    data = []
    for item in plotdata :
        pointname = item['name']
        if item['case'] == 'identicals' :
            pointsize = 14
            pointsymbol = 'square'
        else :
            pointsize = 6
            pointsymbol = 'circle'

        trace = go.Scatter3d(
            x=[item['x']],
            y=[item['y']],
            z=[item['z']],
            name = pointname.capitalize(),
            mode='markers + text', 
            text= pointname.capitalize(),      
            marker=dict(
                size = pointsize,
                color= item['hexa'],
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
        margin=dict(l=0, r=0, b=0, t=30)
        # xaxis='R',
        # yaxis='G',
        # zaxis='Z'
    )
    fig = go.Figure(data=data, layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div