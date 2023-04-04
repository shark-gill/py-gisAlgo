#%%
# Lesson2 - Sptatial data IO

#%%
# 01_Reading Shp file
import geopandas as gpd # Import necessary modules

file_path = "/home/lhshrk/py-gisAlgo/data/DAMSELFISH_distributions.shp"

data = gpd.read_file(file_path)

type(data) # geopandas.geodataframe.GeoDataFrame
data.head()
print(data)
# %%
data.plot()

# %%
# 02_Writing Shp file
# Create a output path for the data
out_file_path = r"/home/lhshrk/py-gisAlgo/data/DAMSELFISH_distributions_Selection.shp"

selection = data[0:50] # Select first 50 rows
selection.to_file(out_file_path) # Write those rows into a new Shapefile (the default output file format is Shapefile)

#%%
# 03_Geometries in Geopandas
"""
iterrows()는 DataFrame의 각 행의 정보를 담은 객체라고 볼 수 있음
"""

data['geometry'].head()
selection2 = data[0:5]

for index, row in selection2.iterrows():
    poly_area = row['geometry'].area
    print("Polygon area at index {0} is: {1:.3f}".format(index, poly_area))

#%%
# dataframe 'area' 컬럼 추가
"""
round(number, digit)
number: 반올림을 적용할 숫자
digit: 반올림하여 얻은 결과에 소수점이 몇 개나 있을지에 대한 숫자
"""
data['area'] = data.area

max_area = data['area'].max() # 최대 면적
min_area = data['area'].min() # 최소 면적
mean_area = data['area'].mean() # 평균 면적

print("Max area: %s\nMin area: %s\nMean area: %s" % (round(max_area, 2), round(min_area, 2), round(mean_area, 2)))

# %%
# 04_Creating geometries into a GeoDataFrame
# Import necessary modules first
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon
import fiona
from fiona.crs import from_epsg

# Create an empty geopandas GeoDataFrame
newdata = gpd.GeoDataFrame()
# print(newdata)
newdata['geometry'] = None # Create a new column called 'geometry' to the GeoDataFrame

coordinates = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coordinates)
newdata.loc[0, 'geometry'] = poly
newdata.loc[0, 'Location'] = 'Senaatintori'
# print(newdata.crs) # None

newdata.crs = from_epsg(4326) # Set the GeoDataFrame's coordinate system to WGS84

# newdata.crs
outfp = r"/home/lhshrk/py-gisAlgo/data/Senaatintori.shp"

newdata.to_file(outfp)
# %%
# 05_Practical example: Save multiple Shapefiles
import geopandas as gpd

shp_fp = "/home/lhshrk/py-gisAlgo/data/DAMSELFISH_distributions.shp"
dataset = gpd.read_file(shp_fp)
"""
groupby()는 데이터를 그룹별로 분할하여 독립된 그룹에 대하여 별도로 데이터를 처리 및 적용하거나 통계량을 확인하고자할 때 사용되는 함수임
"""
group = dataset.groupby('BINOMIAL') 

print(type(dataset)) # <class 'geopandas.geodataframe.GeoDataFrame'>
print(type(group)) # <class 'pandas.core.groupby.generic.DataFrameGroupBy'>

for key, values in group:
    # print(key)
    # print(values)
    individual_fish  =  values

individual_fish
type(individual_fish) # geopandas.geodataframe.GeoDataFrame
print (key) 

# %%
import os
# Determine outputpath
outFolder = r"/home/lhshrk/py-gisAlgo/data"

# Create a new folder called 'Results' (if does not exist) to that folder using os.makedirs() function
resultFolder = os.path.join(outFolder, 'Results')
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)

# Iterate over the
for key, values in group:
    # Format the filename (replace spaces with underscores)
    # replace(left, right)
    # left: 해당되는 문자열을,
    # right: 의 문자열로 변경해라
    outName = "%s.shp" % key.replace(" ", "_")
    # Print some information for the user
    print("Processing: %s" % key)
    # Create an output path
    outpath = os.path.join(resultFolder, outName)

    # Export the data
    values.to_file(outpath)
# %%
