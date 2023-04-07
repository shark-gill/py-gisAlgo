# Lesson5

#%%
## 01_ Static maps
import geopandas as gpd
import matplotlib.pyplot as plt

grid_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/TravelTimes_to_5975375_RailwayStation.shp"
road_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/roads.shp"
metro_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/metro.shp"

grid = gpd.read_file(grid_fp)
road = gpd.read_file(road_fp)
metro = gpd.read_file(metro_fp)

# Get the CRS of the grid, road, metro
gridCRS = grid.crs # EPSG:3067
roadCRS = road.crs # EPSG: 2392
metroCRS = metro.crs # EPSG: 2392

# Reproject geometries using the crs of travel time grid
road['geometry'] = road['geometry'].to_crs(gridCRS)
metro['geometry'] = metro['geometry'].to_crs(gridCRS)
#%%
# Visualize the travel times into 9 classes using "Quantiles" classification scheme
# Add also a little bit of transparency with `alpha` parameter
# (ranges from 0 to 1 where 0 is fully transparent and 1 has no transparency)
my_map = grid.plot(column="car_r_t", linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)

# Add roads on top of the grid
# (use ax parameter to define the map on top of which the second items are plotted)
road.plot(ax=my_map, color="grey", linewidth=1.5)

# Add metro on top of the previous map
metro.plot(ax=my_map, color="red", linewidth=2.5)

# Remove the empty white-space around the axes
plt.tight_layout()
# %%
# Save the figure as png file with resolution of 300 dpi
outfp = r"/home/lhshrk/py-gisAlgo/data/l5_data/static_map.png"
plt.savefig(outfp, dpi=300)

# %%
## 02_Interactive maps
from bokeh.plotting import figure, save

p = figure(title="My first interactive plot!")

x_coords = [0,1,2,3,4]
y_coords = [5,4,1,2,0]

p.circle(x=x_coords, y=y_coords, size=10, color="red")

outfp = r"/home/lhshrk/py-gisAlgo/data/l5_data/points.html"
save(obj=p, filename=outfp)

# %%
## 02-1_Creating interactive maps using Bokeh and Geopandas
import geopandas as gpd

# File path
points_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/addresses.shp"

# Read the data
points = gpd.read_file(points_fp)
points.head()

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

points['x'] = points.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
points['y'] = points.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

points.head()
# %%
# Make a copy and drop the geometry column
p_df = points.drop('geometry', axis=1).copy()
p_df.head(2)
# %%
from bokeh.models import ColumnDataSource

psource = ColumnDataSource(p_df)

psource # ColumnDataSource(	id = 'p1183', …)

# %%
p = figure(title="A map of address points from a Shapefile")
p.circle('x', 'y', source=psource, color='red', size=10)

outfp = r"/home/lhshrk/py-gisAlgo/data/l5_data/point_map.html"

save(p, outfp)

# %%
## 02-2_Adding interactivity to the map
from bokeh.models import HoverTool
my_hover = HoverTool()

my_hover.tooltips = [('Address of the point', '@address')]

p.add_tools(my_hover)

outfp = r"/home/lhshrk/py-gisAlgo/data/l5_data/point_map_hover.html"

save(p, outfp)

# %%
## 02-3_Line map
import geopandas as gpd
from bokeh.models import ColumnDataSource

# File path
metro_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/metro.shp"

# Read the data
metro = gpd.read_file(metro_fp)

def getLineCoords(row, geom, coord_type):
    """Returns a list of coordinates ('x' or 'y') of a LineString geometry"""
    if coord_type == 'x':
        return list( row[geom].coords.xy[0] )
    elif coord_type == 'y':
        return list( row[geom].coords.xy[1] )
    
metro['x'] = metro.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
metro['y'] = metro.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

metro.head()

m_df = metro.drop('geometry', axis=1).copy()
msource = ColumnDataSource(m_df)

p = figure(title="A map of the Helsinki metro")
p.multi_line('x', 'y', source=msource, color='red', line_width=3)
outfp = "/home/lhshrk/py-gisAlgo/data/l5_data/metro_map.html"
save(p, outfp)

# %%
## 02-3Polygon map with Points and Lines
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
import geopandas as gpd
import pysal.viz.mapclassify as ps


# file paths
grid_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/TravelTimes_to_5975375_RailwayStation.shp"
points_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/addresses.shp"
metro_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/metro.shp"

# read file
grid = gpd.read_file(grid_fp)
points = gpd.read_file(points_fp)
metro = gpd.read_file(metro_fp)

standardCRS = grid.crs # EPSG: 3067

points['geometry'] = points['geometry'].to_crs(crs=standardCRS)
metro['geometry'] = metro['geometry'].to_crs(crs=standardCRS)

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y

def getLineCoords(row, geom, coord_type):
    """Returns a list of coordinates ('x' or 'y') of a LineString geometry"""
    if coord_type == 'x':
        return list( row[geom].coords.xy[0] )
    elif coord_type == 'y':
        return list( row[geom].coords.xy[1] )
    
def getPolyCoords(row, geom, coord_type):
    """Returns the coordinates ('x' or 'y') of edges of a Polygon exterior"""

    # Parse the exterior of the coordinate
    exterior = row[geom].exterior

    if coord_type == 'x':
        # Get the x coordinates of the exterior
        return list( exterior.coords.xy[0] )
    elif coord_type == 'y':
        # Get the y coordinates of the exterior
        return list( exterior.coords.xy[1] )

#%%
grid['x'] = grid.apply(getPolyCoords, geom='geometry', coord_type='x', axis=1)
grid['y'] = grid.apply(getPolyCoords, geom='geometry', coord_type='y', axis=1)

metro['x'] = metro.apply(getLineCoords, geom='geometry', coord_type='x', axis=1)
metro['y'] = metro.apply(getLineCoords, geom='geometry', coord_type='y', axis=1)

points['x'] = points.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
points['y'] = points.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

grid.head(2)
# grid[['x', 'y']].head(2)

# %%
# Replace No Data values (-1) with large number (999)
grid = grid.replace(-1, 999)
grid.head(2)

#%%
# Classify our travel times into 5 minute classes until 200 minutes
# Create a list of values where minumum value is 5, maximum value is 200 and step is 5.
breaks = [x for x in range(5, 200, 5)]

#%%
# Initialize the classifier and apply it

classifier = ps.User_Defined.make(bins=breaks)
pt_classif = grid[['pt_r_tt']].apply(classifier)

# Rename the classified column
pt_classif.columns = ['pt_r_tt_ud']

grid.head(3)
# pt_classif.head(3)

#%%

# Join it back to the grid layer
grid['pt_r_tt_ud'] = pt_classif['pt_r_tt_ud']

#%%
# grid.head(1)
# Make a copy, drop the geometry column and create ColumnDataSource
m_df = metro.drop('geometry', axis=1).copy()
msource = ColumnDataSource(m_df)

# Make a copy, drop the geometry column and create ColumnDataSource
p_df = points.drop('geometry', axis=1).copy()
psource = ColumnDataSource(p_df)

# Make a copy, drop the geometry column and create ColumnDataSource
g_df = grid.drop('geometry', axis=1).copy()
gsource = ColumnDataSource(g_df)
# %%
# Let's first do some coloring magic that converts the color palet into map numbers (it's okey not to understand)
from bokeh.palettes import RdYlBu11 as palette
from bokeh.models import LogColorMapper

# Create the color mapper
color_mapper = LogColorMapper(palette=palette)

# Initialize our figure
p = figure(title="Travel times with Public transportation to Central Railway station")

# Plot grid
p.patches('x', 'y', source=gsource,
         fill_color={'field': 'pt_r_tt_ud', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.05)

# Add metro on top of the same figure
p.multi_line('x', 'y', source=msource, color="red", line_width=2)

# Add points on top (as black points)
p.circle('x', 'y', size=3, source=psource, color="black")

# Save the figure
outfp = r"/home/lhshrk/py-gisAlgo/data/l5_data/travel_time_map.html"
save(p, outfp)

# %%
## 03_Advanced plotting with Bokeh
from bokeh.palettes import YlOrRd6 as palette
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, GeoJSONDataSource
from bokeh.palettes import RdYlGn10 as palette
import geopandas as gpd
import pysal.viz.mapclassify as ps
import numpy as np

# Def File Path
fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/TravelTimes_to_5975375_RailwayStation.shp"
roads_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/roads.shp"
metro_fp = r"/home/lhshrk/py-gisAlgo/data/l5_data/metro.shp"

# Read File
data = gpd.read_file(fp)
roads = gpd.read_file(roads_fp)
metro = gpd.read_file(metro_fp)

print(roads['geometry'].geom_type)
#%%

data['geometry'] = data['geometry'].to_crs(epsg=3067)
roads['geometry'] = roads['geometry'].to_crs(epsg=3067)
metro['geometry'] = metro['geometry'].to_crs(epsg=3067)

#%%
def getXYCoords(geometry, coord_type):
    """ Returns either x or y coordinates from  geometry coordinate sequence. Used with LineString and Polygon geometries."""
    if coord_type == 'x':
        return geometry.coords.xy[0]
    elif coord_type == 'y':
        return geometry.coords.xy[1]

def getPolyCoords(geometry, coord_type):
    """ Returns Coordinates of Polygon using the Exterior of the Polygon."""
    ext = geometry.exterior
    return getXYCoords(ext, coord_type)

def getLineCoords(geometry, coord_type):
    """ Returns Coordinates of Linestring object."""
    if geometry.geom_type == 'LineString':
        return getXYCoords(geometry, coord_type)
    elif geometry.geom_type == 'MultiLineString':
        coord_arrays = []
        for part in geometry:
            coord_arrays.append(getXYCoords(part, coord_type))
        return np.concatenate(coord_arrays)


def getPointCoords(geometry, coord_type):
    """ Returns Coordinates of Point object."""
    if coord_type == 'x':
        return geometry.x
    elif coord_type == 'y':
        return geometry.y

def multiGeomHandler(multi_geometry, coord_type, geom_type):
    """
    Function for handling multi-geometries. Can be MultiPoint, MultiLineString or MultiPolygon.
    Returns a list of coordinates where all parts of Multi-geometries are merged into a single list.
    Individual geometries are separated with np.nan which is how Bokeh wants them.
    # Bokeh documentation regarding the Multi-geometry issues can be found here (it is an open issue)
    # https://github.com/bokeh/bokeh/issues/2321
    """
    for i, part in enumerate(multi_geometry): # enumerate(): 
        # On the first part of the Multi-geometry initialize the coord_array (np.array)
        if i == 0:
            if geom_type == "MultiPoint":
                coord_arrays = np.append(getPointCoords(part, coord_type), np.nan)
            elif geom_type == "MultiLineString":
                coord_arrays = np.append(getLineCoords(part, coord_type), np.nan)
            elif geom_type == "MultiPolygon":
                coord_arrays = np.append(getPolyCoords(part, coord_type), np.nan)
        else:
            if geom_type == "MultiPoint":
                coord_arrays = np.concatenate([coord_arrays, np.append(getPointCoords(part, coord_type), np.nan)])
            elif geom_type == "MultiLineString":
                coord_arrays = np.concatenate([coord_arrays, np.append(getLineCoords(part, coord_type), np.nan), np.nan])
            elif geom_type == "MultiPolygon":
                coord_arrays = np.concatenate([coord_arrays, np.append(getPolyCoords(part, coord_type), np.nan)])
    # Return the coordinates
    return coord_arrays

def getCoords(row, geom_col, coord_type):
    """
    Returns coordinates ('x' or 'y') of a geometry (Point, LineString or Polygon) as a list (if geometry is LineString or Polygon).
    Can handle also MultiGeometries.
    """
    # Get geometry
    geom = row[geom_col]
    # Check the geometry type
    gtype = geom.geom_type

    # "Normal" geometries
    # -------------------
    if gtype == "Point":
        return getPointCoords(geom, coord_type)
    elif gtype == "LineString":
        return list(getLineCoords(geom, coord_type))
    elif gtype == "Polygon":
        return list(getPolyCoords(geom, coord_type))
    # Multi geometries
    # ----------------
    else:
        return list(multiGeomHandler(geom, coord_type, gtype))


#%%
data['x'] = data.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
data['y'] = data.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)
data.head(3)
#%%
metro['x'] = metro.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
metro['y'] = metro.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)
metro.head(3)
#%%
roads['x'] = roads.apply(getCoords, geom_col="geometry", coord_type="x", axis=1)
roads['y'] = roads.apply(getCoords, geom_col="geometry", coord_type="y", axis=1)
# roads.head()


# --------★ Fail...... ㅠㅠ
#%%

data = data.replace(-1, 999)
breaks = [x for x in range(5, 200, 5)]
classifier = ps.User_Defined.make(bins=breaks)

pt_classif = data[['pt_r_tt']].apply(classifier)
car_classif = data[['car_r_t']].apply(classifier)

pt_classif.columns = ['pt_r_tt_ud']
car_classif.columns = ['car_r_t_ud']

data['pt_r_tt_ud'] = pt_classif['pt_r_tt_ud']
data['car_r_t_ud'] = car_classif['car_r_t_ud']
# %%
upper_limit = 60
step = 5
names = ["%s-%s " % (x-5, x) for x in range(step, upper_limit, step)]
names.append("%s <" % upper_limit)
data['label_pt'] = None
data['label_car'] = None

for i in range(len(names)):
    data.loc[data['pt_r_tt_ud'] == i, 'label_pt'] = names[i]
    data.loc[data['car_r_t_ud'] == i, 'label_car'] = names[i]

data['label_pt'] = data['label_pt'].fillna("%s <" % upper_limit)
data['label_car'] = data['label_car'].fillna("%s <" % upper_limit)

#%%
# Select only necessary columns for our plotting to keep the amount of data minumum
df = data[['x', 'y', 'pt_r_tt_ud', 'pt_r_tt', 'car_r_t', 'from_id', 'label_pt']]
dfsource = ColumnDataSource(data=df)

# Include only coordinates from roads (exclude 'geometry' column)
rdf = roads[['x', 'y']]
rdfsource = ColumnDataSource(data=rdf)

# Include only coordinates from metro (exclude 'geometry' column)
mdf = metro[['x','y']]
mdfsource = ColumnDataSource(data=mdf)

# Specify the tools that we want to use
TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

# Flip the colors in color palette
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

p = figure(title="Travel times to Helsinki city center by public transportation", tools=TOOLS,
           plot_width=650, plot_height=500, active_scroll = "wheel_zoom" )

# Do not add grid line
p.grid.grid_line_color = None

# Add polygon grid and a legend for it
grid = p.patches('x', 'y', source=dfsource, name="grid",
         fill_color={'field': 'pt_r_tt_ud', 'transform': color_mapper},
         fill_alpha=1.0, line_color="black", line_width=0.03, legend="label_pt")

# Add roads
r = p.multi_line('x', 'y', source=rdfsource, color="grey")

# Add metro
m = p.multi_line('x', 'y', source=mdfsource, color="red")

# Modify legend location
p.legend.location = "top_right"
p.legend.orientation = "vertical"

# Insert a circle on top of the Central Railway Station (coords in EurefFIN-TM35FIN)
station_x = 385752.214
station_y =  6672143.803
circle = p.circle(x=[station_x], y=[station_y], name="point", size=6, color="yellow")

# Add two separate hover tools for the data
phover = HoverTool(renderers=[circle])
phover.tooltips=[("Destination", "Railway Station")]

ghover = HoverTool(renderers=[grid])
ghover.tooltips=[("YKR-ID", "@from_id"),
                ("PT time", "@pt_r_tt"),
                ("Car time", "@car_r_t"),
               ]

p.add_tools(ghover)
p.add_tools(phover)

# Output filepath to HTML
output_file = r"/home/lhshrk/py-gisAlgo/data/l5_data/accessibility_map_Helsinki.html"

# Save the map
save(p, output_file)

# %%

# [추후작업]Interactive maps on Leaflet