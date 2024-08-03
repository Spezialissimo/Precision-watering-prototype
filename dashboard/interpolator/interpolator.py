import numpy as np
from scipy.interpolate import interpn

def interpolate_data(data, x_values, y_values):
    values_grid = np.full((len(x_values), len(y_values)), np.nan)
    for value in data:
        x_idx = x_values.index(value["x"])
        y_idx = y_values.index(value["y"])
        values_grid[x_idx, y_idx] = value["v"]

    x_range = np.linspace(min(x_values), max(x_values), num=21)
    y_range = np.linspace(min(y_values), max(y_values), num=21)

    x_grid, y_grid = np.meshgrid(x_range, y_range)
    xi = np.vstack([x_grid.ravel(), y_grid.ravel()]).T

    interpolated_values = interpn((x_values, y_values), values_grid, xi, method='linear', bounds_error=False, fill_value=0)

    new_data = []
    for i, point in enumerate(xi):
        new_data.append({
            "x": int(point[0]),
            "y": int(point[1]),
            "v": float(interpolated_values[i])
        })

    return new_data
