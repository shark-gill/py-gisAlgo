#%%
# Lesson3

#%%
# 01_Geocoding
"""
Geocoding은 주소(ex: 경기도 안산시 단원구 지곡로 4길 22)를 좌표(ex: 126.xxxxx, 36.xxxxx)로 변환하는 데이터 처리 절차임

"""
# import moudles
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas.tools import geocode

"""
r: raw string literal을 의미하며, \이스케이프 코드로 인식하지 않고 문자열을 모두 출력할 수 있음
"""
file_path = r"/home/lhshrk/py-gisAlgo/data/addresses.txt"


data = pd.read_csv(file_path, sep=';')

data.addr # addr 컬럼에 있는 값을 반환

# data.head()

geo = geocode(data.addr) # addr 컬럼을 지오코딩

geo # table(geometry + address)
geo.crs # wgs 84: EPSG4326 // 
type(geo) # geopandas.geodataframe.GeoDataFrame

#%%
out_file_path = r"/home/lhshrk/py-gisAlgo/data/addresses.shp"

geo.to_file(out_file_path)
# %%
# 02_Point in Polygon & Intersect
from shapely.geometry import Point, Polygon, LineString, MultiLineString

# Create Point objects
p1 = Point(24.952242, 60.1696017)
p2 = Point(24.976567, 60.1612500)

# Create a Polygon
coords = [(24.950899, 60.169158), (24.953492, 60.169158), (24.953510, 60.170104), (24.950958, 60.169990)]
poly = Polygon(coords)
poly


poly_centroid = poly.centroid

p1_poly = p1.within(poly)
p2_poly = p2.within(poly)
cent_poly = poly_centroid.within(poly)

# 폴리곤 내부에 포인트가 존재하나?
p1_poly # True
p2_poly # False
cent_poly # True

# 포함 여부
print(poly.contains(p1)) # True
print(poly.contains(p2)) # False
print(poly.contains(poly_centroid)) # True

# %%
# Intersect & Touch Check
point1 = Point(0, 0)
point2 = Point(1, 1)
point3 = Point(1, 1)
point4 = Point(0, 2)

line_a = LineString([point1, point2])
line_b = LineString([point3, point4])
mult_line = MultiLineString([line_a, line_b])

print(line_a.intersects(line_b)) # True
print(line_a.touches(line_b)) # True
print(line_a.intersects(line_a)) # True
print(line_a.touches(line_a)) # False


# %%
# Point in Polygon Using Geopandas
import geopandas as gpd

fp = r"/home/lhshrk/py-gisAlgo/data/addresses.shp"
point_dataset = gpd.read_file(fp, driver='')

point_dataset
# %%
import geopandas as gpd
import matplotlib.pyplot as plt

gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

fp2 = r"/home/lhshrk/py-gisAlgo/data/PKS_suuralue.kml"

poly_dataset = gpd.read_file(fp2, driver='KML')
poly_dataset

# %%
southern = poly_dataset[poly_dataset['Name'] == 'Eteläinen']

# print(southern) // 'Eteläinen'에 해당하는 행 값만을 출력
"""
drop=True: 추출된 컬럼의 index를 버리고,
inplace=True: index를 재배열 해줌
"""
southern.reset_index(drop=True, inplace=True)

fig, ax = plt.subplots()
poly_dataset.plot(ax=ax, facecolor='gray')
southern.plot(ax=ax, facecolor='red')
point_dataset.plot(ax=ax, color='blue', markersize=5)

# plt.show()
plt.tight_layout()


# %%
# point in Polygon Spatial query
import shapely.speedups as spu

spu.enable() # spu -> 허용함

pip_mask = point_dataset.within(southern.loc[0, 'geometry'])
# pip_mask
pip_data = point_dataset.loc[pip_mask]
# pip_data

southern = poly_dataset[poly_dataset['Name']=='Eteläinen']
southern.reset_index(drop=True, inplace=True)
fig, ax = plt.subplots()
poly_dataset.plot(ax=ax, facecolor='gray')
southern.plot(ax=ax, facecolor='red')
pip_data.plot(ax=ax, color='gold', markersize=2)
plt.tight_layout()

# %%
# 03_Spatial Join
"""
공간조인(Spatial Join): 두 개 이상의 데이터셋을 공간 관계를 기준으로 서로 연결하는 연산 방법임
1) intersects: 2개의 공간 객체가 교차하는지 검사
2) disjoint: 2개의 공간 객체에 공통 요소가 없는지 검사
3) contains: 공간 객체가 다른 객체를 포함하는지 검사
4) within: 공간 객체가 다른 객체 내부에 있는지 검사
5) touches: 2개의 공간객체가 맞닿아 있는지 검사
6) crosses: 2개의 공간 객체가 서로 횡단하는지 검사
7) overlaps: 2개의 공간 객체가 서로 겹치는지 검사
8) equals: 2개의 공간 개체가 위상적으로 동일한지 검사
"""

#%%
# dataset
# url: https://hri.fi/data/en_GB/dataset/vaestotietoruudukko
# unzip: unzip {filename} -d {folder}, format(Vaestotietoruudukko_2015.zip, l3_data) / 안됨 ㅠ

import geopandas as gpd

# FilePath
fp = r'/home/lhshrk/py-gisAlgo/data/Vaestotietoruudukko_2021_shp/Vaestotietoruudukko_2021.shp'
addr_fp = r'/home/lhshrk/py-gisAlgo/data/addresses.shp'

# Read the data
pop = gpd.read_file(fp)
addr = gpd.read_file(addr_fp)

print(pop.head(), pop.columns)
print("--------------------------")
print(addr.head(), addr.columns)
#%%

pop = pop.rename(columns = {'ASUKKAITA': 'pop15'})
pop.columns
print(pop.head(), pop.columns)
#%%

selected_cols = ['pop15', 'geometry'] # 분석에 필요한 컬럼만 추출

pop_dataset = pop[selected_cols]
print(pop_dataset.head(), pop_dataset.columns)

print(pop_dataset.crs) # EPSG:3879
# print(addr.crs) # EPSG:4326

addr_epsg3879 = addr.to_crs(epsg=3879)
addr_epsg3879.head()

# print(addr_epsg3879.crs)
#%%
addr_epsg3879_out_file_path = r"/home/lhshrk/py-gisAlgo/data/addresses_epsg3879.shp"

addr_epsg3879.to_file(addr_epsg3879_out_file_path)

# %%
join = gpd.sjoin(addr_epsg3879, pop_dataset, how="inner", op="within")
join

#%%
out_fp = r'/home/lhshrk/py-gisAlgo/data/addresses_pop15_epsg3879.shp'

join.to_file(out_fp)

# %%
import matplotlib.pyplot as plt

# Plot the points with population info
join.plot(column='pop15', cmap="Reds", markersize=7, scheme='natural_breaks', legend=True);

# Add title
plt.title("Amount of inhabitants living close the the point")

# Remove white space around the figure
plt.tight_layout()

# %%
# 04_Nearest Neighbour Analysis
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points

orig = Point(1, 1.67)
dest1, dest2, dest3 = Point(0, 1.45), Point(2, 2), Point(0, 2.5)
destinations = MultiPoint([dest1, dest2, dest3])
# destinations

# %%
nearest_geoms = nearest_points(orig, destinations)

near_idx0 = nearest_geoms[0] # origin
near_idx1 = nearest_geoms[1] # dest 중 가장 가까운 점

nearest_geoms
#%%

def Nearest(row, geom_union, df1, df2, geom1_col='geometry', geom2_col='geometry', src_column=None):
    """Find the nearest point and return the corresponding value from specified column."""
    # Find the geometry that is closest
    nearest = df2[geom2_col] == nearest_points(row[geom1_col], geom_union)[1]
    # Get the corresponding value from df2 (matching is based on the geometry)
    value = df2[nearest][src_column].get_values()[0]
    print(type(value))
    return value

# %%
import geopandas as gpd
import matplotlib.pyplot as plt
from fiona.drvsupport import supported_drivers

supported_drivers['KML'] = 'rw'

#%%

fp1 = "/home/lhshrk/py-gisAlgo/data/PKS_suuralue.kml"
fp2 = "/home/lhshrk/py-gisAlgo/data/addresses.shp"

df1 = gpd.read_file(fp1, driver='KML')
df2 = gpd.read_file(fp2)

print(df1.head())
print(df2.head())
# %%
unary_union = df2.unary_union # Point -> MultiPoint
print(unary_union)

#%%
df1['cetroid'] = df1.centroid
df1.head()

# %%
df1['nearest_id'] = df1.apply(Nearest, geom_union=unary_union, df1=df1, df2=df2, geom1_col='cetroid', src_column='geometry', axis=1)

df1.head(10)
# %%
