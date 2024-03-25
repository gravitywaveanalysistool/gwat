import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate

import metpy.calc as mpcalc
from metpy.plots import Hodograph
from metpy.units import units
from matplotlib.cm import get_cmap

def graph2d(x, y, deg, x_label, y_label, title):
    # Scatter plot
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=5, label='Data Points')

    # Best fit curve
    coeffs = np.polyfit(y, x, deg)
    y_curve = np.linspace(min(y), max(y), 500)
    x_curve = np.polyval(coeffs, y_curve)

    ax.plot(x_curve, y_curve, 'r-', label='Best Fit Line')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()

    return fig

def calcWindComps(speeds, directions):
    speeds = np.array(speeds)
    directions = np.array(directions)

    u = -speeds * np.sin(np.radians(directions))
    v = -speeds * np.cos(np.radians(directions))
    return u, v

def hodograph(compRange, lineWidth, profile_df):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(1, 1, 1)
    hodo = Hodograph(ax, component_range=compRange)
    hodo.add_grid(increment=10)
    hodo.add_grid(increment=20, linestyle='-')

    # Convert all values in the DataFrame to numeric
    profile_df_numeric = profile_df.map(pd.to_numeric, errors='coerce')

    # colormap
    cmap = get_cmap('viridis')
    norm = plt.Normalize(vmin=profile_df_numeric['Alt'].min(), vmax=profile_df_numeric['Alt'].max())

    # Calculate wind components
    speeds = profile_df_numeric['Ws']
    directions = profile_df_numeric['Wd']
    u, v = calcWindComps(speeds, directions)

    # Plot hodograph segments with altitude-based coloring
    for i in range(len(u) - 1):
        segment_color = cmap(norm(profile_df_numeric['Alt'].iloc[i]))
        ax.plot([0, u[i]], [0, v[i]], color=segment_color, linewidth=lineWidth,
                label=f'{profile_df_numeric["Alt"].iloc[i]:.0f}-{profile_df_numeric["Alt"].iloc[i + 1]:.0f} m')

    # Create altitude color bar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cb = fig.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046, pad=0.04)
    cb.set_label('Altitude (m)')

    # Set axis labels
    ax.set_xlabel('U Component (m/s)')
    ax.set_ylabel('V Component (m/s)')

    return fig