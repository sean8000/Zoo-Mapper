import numpy as np
from scipy import stats
from mayavi import mlab
import pandas as pd
import csv

BANDWIDTH = 0.95

# Data file for testing
filename = 'C:/Users/Kevin/Documents/CISC498/Sample Data for 3D Distances.xlsx'

# Read Data from test file
data = pd.read_excel(filename)

j_data = data[data['Focal_Shar'] == 'J']

d_data = data[data['Focal_Shar'] == 'D']

x = d_data['LongUTM']
y = d_data['LatUTM']
z = d_data['DepthM']

noise = np.random.normal(0, 1, z.shape)
z = z + noise

jx = j_data['LongUTM']
jy = j_data['LatUTM']
jz = j_data['LatUTM']

j_noise = np.random.normal(0, 1, jz.shape)
jz = jz + j_noise

xyz = np.vstack([x,y,z])
kde = stats.gaussian_kde(xyz)
kde.set_bandwidth(BANDWIDTH)

j_xyz = np.vstack([jx, jy, jz])
j_kde = stats.gaussian_kde(j_xyz)
j_kde.set_bandwidth(BANDWIDTH)

xmin, ymin, zmin = x.min(), y.min(), z.min()
xmax, ymax, zmax = x.max(), y.max(), z.max()
xi, yi, zi = np.mgrid[xmin:xmax:30j, ymin:ymax:30j, zmin:zmax:30j]
coords = np.vstack([item.ravel() for item in [xi, yi, zi]])
density = kde(coords).reshape(xi.shape)

j_xmin, j_ymin, j_zmin = jx.min(), jy.min(), jz.min()
j_xmax, j_ymax, j_zmax = jx.max(), jy.max(), jz.max()
j_xi, j_yi, j_zi = np.mgrid[j_xmin:j_xmax:30j, j_ymin:j_ymax:30j, j_zmin:j_zmax:30j]
j_coords = np.vstack([item.ravel() for item in [j_xi, j_yi, j_zi]])
j_density = j_kde(j_coords).reshape(j_xi.shape)

# Plot with mayavi
figure = mlab.figure('DensityPlot')

# grid = mlab.pipeline.scalar_field(xi, yi, zi, density)
# min = density.min()
# max = density.max()
# mlab.pipeline.volume(grid, vmin=min, vmax=max+0.5*(max-min))

j_grid = mlab.pipeline.scalar_field(j_xi, j_yi, j_zi, j_density)
j_min = j_density.min()
j_max = j_density.max()
mlab.pipeline.volume(j_grid, vmin=j_min, vmax=j_max+0.5*(j_max-j_min))

mlab.axes()
mlab.show()

# # Plot scatter with mayavi
# figure = mlab.figure('DensityPlot')
# figure.scene.disable_render = True

# pts = mlab.points3d(x, y, z, density, scale_mode='none', scale_factor=0.07)
# mask = pts.glyph.mask_points
# mask.maximum_number_of_points = x.size
# mask.on_ratio = 1
# pts.glyph.mask_input_points = True

# figure.scene.disable_render = False
# mlab.axes()
# mlab.show()
