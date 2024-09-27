import numpy as np
import plotly.graph_objs as go

def create_rectangle(x, y, step = 1, y_offset = 230):
    points = []
    
    # Horizontal boundaries: from -x/2 to x/2
    x_min = -x / 2
    x_max = x / 2
    
    # Bottom side (moving right from x_min to x_max)
    for xi in np.arange(x_min, x_max + step, step):
        points.append([xi, 0 + y_offset])
    
    # Right side (moving up from 0 to y)
    for yi in np.arange(0, y + step, step):
        points.append([x_max, yi + y_offset])
    
    # Top side (moving left from x_max to x_min)
    for xi in np.arange(x_max, x_min - step, -step):
        points.append([xi, y + y_offset])
    
    # Left side (moving down from y to 0)
    for yi in np.arange(y, 0 - step, -step):
        points.append([x_min, yi + y_offset])
    
    return points


def plot_rectangle_path(rect_points):
    # Separate x and y coordinates
    x_coords = [point[0] for point in rect_points]
    y_coords = [point[1] for point in rect_points]
    
    # Close the rectangle by appending the starting point at the end
    x_coords.append(rect_points[0][0])
    y_coords.append(rect_points[0][1])
    
    # Create the plot using Plotly
    trace = go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='lines+markers',
        name='Rectangle Path',
        line=dict(color='royalblue', width=2),
        marker=dict(size=4)
    )
    
    layout = go.Layout(
        title='Rectangle Path',
        xaxis=dict(title='X (mm)'),
        yaxis=dict(title='Y (mm)'),
        showlegend=False,
        width=600,
        height=600
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    fig.show()