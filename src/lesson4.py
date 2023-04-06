# Lesson4

#%%
## Data reclassification

# 01_Data Download
# url: https://github.com/Automating-GIS-processes/Lesson-4-Classification-overlay/raw/master/data/data.zip
# path: /home/lhshrk/py-gisAlgo/data/l4_data

#%%
# 02_Data preparation
import geopandas as gpd
import matplotlib.pyplot as plt

fp = "/home/lhshrk/py-gisAlgo/data/l4_data"

data = gpd.read_file(fp)

# Select only English columns
selected_cols = ['Level1', 'Level1Eng', 'Level2', 'Level2Eng', 'Level3', 'Level3Eng', 'Luokka3', 'geometry']

pre_data = data[selected_cols]


pre_data.plot(column='Level3', linewidth=0.05)
plt.tight_layout()

# %%
level3eng_type = list(pre_data['Level3Eng'].unique())
level3eng_type

#%%
# Select lakes (i.e. 'waterbodies' in the data) and make a proper copy out of our data
lakes = pre_data[pre_data['Level3Eng'] == 'Water bodies'].copy()
lakes.head(3)

# %%
# 03_Calculations in DataFrames

# Caculate the area of lakes
lakes['area'] = lakes['geometry'].area
lakes['area_km2'] = lakes['area'] / 1000000
l_mean_size = lakes['area_km2'].mean()
l_mean_size


# %%
# 04_Classifying data

def binaryClassifier(data, source_col, output_col, threshold):
    # If area of input geometry is lower that the threshold value
    if data[source_col] < threshold:
        # Update the output column with value 0
        data[output_col] = 0
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        data[output_col] = 1
    # Return the updated row
    return data

lakes['small_big'] = None
lakes = lakes.apply(binaryClassifier, source_col='area_km2', output_col='small_big', threshold=l_mean_size, axis=1)

# Visualization
lakes.plot(column='small_big', linewidth=0.05, cmap="seismic")
plt.tight_layout()

#%%
# output file
outfp_lakes = r"/home/lhshrk/py-gisAlgo/data/l4_data/lakes.shp"
lakes.to_file(outfp_lakes)
# %%

#%%
# 05_Multicriteria data classification

def customClassifier2(row, src_col1, src_col2, threshold1, threshold2, output_col):
    # 1. If the value in src_col1 is LOWER than the threshold1 value
    # 2. AND the value in src_col2 is HIGHER than the threshold2 value, give value 1, otherwise give 0
    if row[src_col1] < threshold1 and row[src_col2] > threshold2:
        # Update the output column with value 0
        row[output_col] = 1
    # If area of input geometry is higher than the threshold value update with value 1
    else:
        row[output_col] = 0

    # Return the updated row
    return row

#%%
# 06_Geometric operations
import geopandas as gpd
import matplotlib.pyplot as plt
import shapely.speedups

# Let's enable speedups to make queries faster
shapely.speedups.enable()

# File paths
border_fp = "/home/lhshrk/py-gisAlgo/data/l4_data/Helsinki_borders.shp"
grid_fp = "/home/lhshrk/py-gisAlgo/data/l4_data/TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp) # EPSG:3067
hel = gpd.read_file(border_fp) # EPSG:3067

basemap = hel.plot()

grid.plot(ax=basemap, facecolor='gray', linewidth=0.02)
result = gpd.overlay(grid, hel, how='intersection')

result.plot(color="b")
plt.tight_layout()

# %%
resultfp = "/home/lhshrk/py-gisAlgo/data/l4_data/TravelTimes_to_5975375_RailwayStation_Helsinki.geojson"

# Use GeoJSON driver
result.to_file(resultfp, driver="GeoJSON")

"""
Polygon의 개수가 많을 때 overlay 분석은 엄청난 컴퓨터 자원을 사용할 수 있기 때문에, 아래와 같이 활용하여 연산의 속도를 줄일 수 있음
---------------

import geopandas as gpd
import numpy as np

# File paths
border_fp = "/home/lhshrk/py-gisAlgo/data/l4_data/Helsinki_borders.shp"
grid_fp = "/home/lhshrk/py-gisAlgo/data/l4_data/TravelTimes_to_5975375_RailwayStation.shp"

# Read files
grid = gpd.read_file(grid_fp)
hel = gpd.read_file(border_fp)

# Batch size
b = 10

# Number of iterations (round up with np.ceil) and convert to integer
row_cnt = len(grid)
iterations = int(np.ceil(row_cnt / b))

# Final result
final = gpd.GeoDataFrame()

# Set the start and end index according the batch size
start_idx = 0
end_idx = start_idx + b

for iteration in range(iterations):
    print("Iteration: %s/%s" % (iteration, iterations))

    # Make an overlay analysis using a subset of the rows
    result = gpd.overlay(grid[start_idx:end_idx], hel, how='intersection')

    # Append the overlay result to final GeoDataFrame
    final = final.append(result)

    # Update indices
    start_idx += b
    end_idx = start_idx + b

# Save the output as GeoJSON
outfp = "/home/lhshrk/py-gisAlgo/data/l4_data/overlay_analysis_speedtest.geojson"
final.to_file(outfp, driver="GeoJSON")

final.plot()

-------
"""
# %%
# Aggregating data
result_aggregated = result.dissolve(by="car_r_t")
result_aggregated.head()

print(len(result)) # 3826
print(len(result_aggregated)) # 51

# %%
# Simplifying geometries

lakes_fp = "/home/lhshrk/py-gisAlgo/data/l4_data/lakes.shp"
lakes = gpd.read_file(lakes_fp)

big_lakes = lakes[lakes['small_big'] == 1].copy()
big_lakes.plot(linewidth=0.05, color='blue')
plt.tight_layout()
print(len(lakes['geometry'])) # 232
# %%
big_lakes['geom_gen'] = big_lakes.simplify(tolerance=300)
big_lakes['geometry'] = big_lakes['geom_gen']

big_lakes.plot(linewidth=0.05, color='blue')
plt.tight_layout()
print(len(big_lakes['geometry'])) # 44
# %%
