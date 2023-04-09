# Lesson7

"""
OpenStreetMap(OSM): 누구나 참여할 수 있는 오픈 소스 방식의 무료 지도 
"""

#%%
## 01_Retrieving OpenStreetMap data
import osmnx as ox
import matplotlib.pyplot as plt

place_name = "Kamppi, Helsinki, Finland"
# place_name = "안산시, 대한민국"
graph = ox.graph_from_place(place_name)


# 경기도 지역의 도로 네트워크 그래프를 가져옴
graph = ox.graph_from_place(place_name, network_type='drive')

# print(type(graph)) # <class 'networkx.classes.multidigraph.MultiDiGraph'>

#%%
fig, ax = ox.plot_graph(graph)
plt.tight_layout()

#%%
# area = ox.gdf_from_place(place_name)
area = ox.geocode_to_gdf(place_name)
# buildings = ox.buildings_from_place(place_name)
buildings = ox.geometries_from_place(place_name, tags={'building':True})


print(area.head(3))
print("---------------")
print(buildings.head(3))
#%%
# Node & Edge Extraction
nodes, edges = ox.graph_to_gdfs(graph)
# nodes.head()
# edges.head()

fig= plt.subplot() 
ax = plt.subplot()

# area.plot(ax=ax, facecolor = 'black')
edges.plot(ax=ax, linewidth = 1, edgecolor= '#BC8F8F')
buildings.plot(ax=ax, facecolor='khaki', alpha = 0.7)

plt.tight_layout()

#%% 
#! Network analysis in Python
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

place_name = "Kamppi, Helsinki, Finland"
graph = ox.graph_from_place(place_name, network_type = 'drive')

fig, ax = ox.plot_graph(graph)



#%%
## 01_Network analysis in Python
import osmnx as ox
import networkx as nx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
place_name = "Kamppi, Helsinki, Finland"
graph = ox.graph_from_place(place_name, network_type='drive')
fig, ax = ox.plot_graph(graph)
# %%
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)
edges.columns
edges['highway'].value_counts()
print(f"crs:{edges.crs}") # CRS: EPSG4326

# %%
graph_proj = ox.project_graph(graph)
fig, ax = ox.plot_graph(graph_proj)
plt.tight_layout()
# %%
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)
print("Coordinate system:", edges_proj.crs)
# %%
status = ox.basic_stats(graph_proj)
status.keys()
# %%
graph_area_m = nodes_proj.unary_union.convex_hull.area
# print(graph_area_m) # 796608.39....
status = ox.basic_stats(graph_proj, area=graph_area_m)
status
 
 #%%
edges_proj.bounds.head()
from shapely.geometry import box
bbox = box(*edges_proj.unary_union.bounds)
# print(bbox)
orig_point = bbox.centroid
orig_point
# %%
nodes_proj['x'] = nodes_proj.x.astype(float)
maxx = nodes_proj['x'].max()
target_loc = nodes_proj.loc[nodes_proj['x']==maxx, :]
print(target_loc)

target_point = target_loc.geometry.values[0]
print(target_point)

#%%
# orig_xy = (orig_point.y, orig_point.x)
# target_xy = (target_point.y, target_point.x)
#%%
orig_node = ox.nearest_nodes(graph_proj, orig_point.x, orig_point.y)
target_node = ox.nearest_nodes(graph_proj, target_point.x, target_point.y)
o_closest = nodes_proj.loc[orig_node]
t_closest = nodes_proj.loc[target_node]

print(orig_node)
print(target_node)

#%%
od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes_proj.crs)
#%%
route = nx.shortest_path(G=graph_proj, source=orig_node, target=target_node, weight='length')
print(route) 
"""
osmnx.plot.plot_graph_route(G, route, route_color='r', route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None, **pg_kwargs)
"""
fig, ax = ox.plot_graph_route(graph_proj, route)
plt.tight_layout()
od_nodes.crs

#%%
route_nodes = nodes_proj.loc[route]
print(route_nodes)

#%%
from shapely.geometry import LineString, Point
route_line = LineString(list(route_nodes.geometry.values))
print(route_line)

print(edges_proj.crs)
#%%

route_geom = gpd.GeoDataFrame()
route_geom['geometry'] = None
route_geom['osmid'] = None
# route_nodes.index.values
route_geom.loc[0, 'osmid'] = str(list(route_nodes.index.values))
route_geom.loc[0 ,'geometry'] = route_line
# route_geom.head(3)
route_geom['length_m'] = route_geom.length
# route_geom.head(6)

route_geom = route_geom.set_crs(crs = edges_proj.crs)
print(route_geom.crs)
#%%
od_points = gpd.GeoDataFrame()
od_points['geometry'] = None
od_points['type'] = None
od_points.loc[0, ['geometry', 'type']] = orig_point, 'Origin'
od_points.loc[1, ['geometry', 'type']] = target_point, 'Target'
od_points.head()
od_points = od_points.set_crs(crs = edges_proj.crs)

#%%
buildings = ox.geometries_from_place(place_name, tags={'building':True})
buildings_proj = buildings.to_crs(crs=edges_proj.crs)
print(buildings.crs)

#%%
fig, ax = plt.subplots()
edges_proj.plot(ax=ax, linewidth=0.75, color='gray')
nodes_proj.plot(ax=ax, markersize=2, color='gray')
buildings_proj.plot(ax=ax, facecolor='khaki', alpha=0.7)
route_geom.plot(ax=ax, linewidth=4, linestyle='--', color='red')
od_points.plot(ax=ax, markersize=24, color='green')
plt.tight_layout()

#%%
# Parse the place name for the output file names (replace spaces with underscores and remove commas)
place_name_out = place_name.replace(' ', '_').replace(',','')
streets_out = r"/home/lhshrk/py-gisAlgo/data/l7_data/%s_streets.shp" % place_name_out
route_out = r"/home/lhshrk/py-gisAlgo/data/l7_data/Route_from_a_to_b_at_%s.shp" % place_name_out
nodes_out = r"/home/lhshrk/py-gisAlgo/data/l7_data/%s_nodes.shp" % place_name_out
buildings_out = r"/home/lhshrk/py-gisAlgo/data/l7_data/%s_buildings.shp" % place_name_out
od_out = r"/home/lhshrk/py-gisAlgo/data/l7_data/%s_route_OD_points.shp" % place_name_out

invalid_cols = ['lanes', 'maxspeed', 'name', 'oneway', 'osmid']
for col in invalid_cols:
    edges_proj[col] = edges_proj[col].astype(str)

edges_proj
#%%
edges_proj.to_file(streets_out)
route_geom.to_file(route_out)
nodes_proj.to_file(nodes_out)
od_points.to_file(od_out)
buildings[['geometry', 'name', 'addr:street']].to_file(buildings_out)
#%%
# Reference
# 국내 적용을 위해서는 아래의 url을 참고하여 예시를 작성할 필요가 있음
# https://anweh.tistory.com/36

# %%
