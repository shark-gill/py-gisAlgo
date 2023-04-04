#%%
# Lesson1 - Geometric Objects

# 01_Abstract
"""
Python을 활용한 공간분석 라이브러리
1) 데이터 분석 및 시각화
- Numpy:  Python을 사용한 과학적 컴퓨팅을 위한 기본 패키지
- Pandas: 다양한 데이터 유형을 구조 및 분석 도구
- Scipy: 데이터 처리 및 최적화, 통계분석을 수행하기 위한 패키지
- Matplotlib: 파이썬을 이용한 시각화 라이브러리
- Bokeh: 웹 기반의 동적 시각화 라이브러리
- Plotly: 웹 기반의 동적 시각화 라이브러리

2) 공간 데이터 처리 및 분석 라이브러리
- GDAL: 벡터 및 래스터 데이터 형식을 처리하기 위한 기본 패키지(아래의 많은 모듈이 이에 의존함). 래스터 처리에 사용됩니다.
- Geopandas: Python에서 지리 공간 데이터 작업이 더 쉬워지고 pandas와 shapely의 기능이 결합됩니다.
- Shapely: 평면 기하학적 개체의 조작 및 분석을 위한 Python 패키지(널리 배포된 GEOS 기반 ).
- Fiona: 공간 데이터 읽기 및 쓰기(geopandas의 대안).
- Pyproj: 지도 제작 변환 및 측지 계산을 수행합니다( PROJ.4 기반 ).
- Pysal: Python으로 작성된 공간 분석 함수 라이브러리.
- Geopy: 지오코딩 라이브러리: 주소를 지정하는 좌표 <-> 주소를 좌표로 지정합니다.
- GeoViews: 웹용 대화형 지도.
- Geoplot: Python용 고급 지리 공간 데이터 시각화 라이브러리.
- Dash: Dash는 분석 웹 애플리케이션을 구축하기 위한 Python 프레임워크입니다.
- OSMnx: 거리 네트워크용 Python. OpenStreetMap에서 거리 네트워크 검색, 구성, 분석 및 시각화
- Networkx: Python의 네트워크 분석 및 라우팅(예: Dijkstra 및 A* -알고리즘)은 이 게시물을 참조하십시오 .
- Cartopy: 데이터 분석 및 시각화를 위한 드로잉 맵을 가능한 한 쉽게 만듭니다.
- Scipy.spatial: 공간 알고리즘 및 데이터 구조.
- Rtree: 빠른 공간 조회를 위한 Python용 공간 인덱싱.
- Rasterio: Python용 깨끗하고 빠른 지형 공간적 래스터 I/O.
- RSGISLib: Python용 원격 감지 및 GIS 소프트웨어 라이브러리.
"""

#%%
# 02_Geometric Objects - Spatial Data Model
"""
기하 객체는 벡터 형식의 공간 데이터로 작업할 때 가장 기본적인 요소인 점, 선, 폴리곤으로 구성되며, 튜플로 정의함
- 점(Point): 공간의 단일 지점을 나타냄. ex: 2D - (x, y), 3D - (x, y, z)
- 선(LineString): 선을 형성하기 위해 점의 집합으로 구성됨
- 폴리곤(Plygon): 폴리곤(polygon)은 3차원 컴퓨터그래픽을 구성하는 가장 기본단위인 다각형을 의미

기하 객체는 여러 개의 집합(Collection)으로 구성될 수 있음
- MultiPoint: 포인트의 집함
- MultiLineString: 선의 집합
- MultiPolygon: 폴리곤의 집합
"""
#%%
# 02-1_Point
# Import necessary geometric objects from shapely module
from shapely.geometry import Point, LineString, Polygon
from pprint import pprint

# Create Point geometric obejct(s) with coordinates
point1 = Point(2.2, 4.2)
point2 = Point(7.2, -25.1)
point3 = Point(9.26, -2.456)

point3D = Point(9.26, -2.456, 0.57)

# What is the type of this? // <class 'shapely.geometry.point.Point'>
pt_type = type(point3D)
print(pt_type) 

# Get the coordinates // <shapely.coords.CoordinateSequence object at 0x7f9d4c330150>
print(point3D.coords)

# Get x and y coordinates // (array('d', [9.26]), array('d', [-2.456]))
print(point3D.xy)

# Whatabout z coordinate? // 0.57
print(point3D.z)

# Calculate the distance between point1 and point2 // Distance between the points is 29.72 decimal degrees
point_dist = point1.distance(point2)
print("Distance between the points is {0:.2f} decimal degrees".format(point_dist))

# %%
# 02-2_LineString

# Create a LineString from our Point objects
line = LineString([point1, point2, point3])

# It is also possible to use coordinate tuples having the same outcome
line2 = LineString([(2.2, 4.2, 4.5), (7.2, -25.1, 6.45), (9.26, -2.456, 7.5)])

print(line) # LINESTRING (2.2 4.2, 7.2 -25.1, 9.26 -2.456)
print(line2) # LINESTRING (2.2 4.2, 7.2 -25.1, 9.26 -2.456)
print(type(line)) # <class 'shapely.geometry.linestring.LineString'>

# Get x and y coordinates of the line // (array('d', [2.2, 7.2, 9.26]), array('d', [4.2, -25.1, -2.456]))
lxy = line.xy
print(lxy)

# Extract x coordinates // 선을 구성하는 모든 x 좌표 추출
line_x = lxy[0]
print(line_x) 

# Extract y coordinates straight from the LineObject by referring to a array at index 1
line_y = lxy[1]
print(line_y) 

# LineString 자체에서 선의 길이와 중심 속성 추출

# Get the lenght of the line // Length of our line: 52.46
l_length = line.length
print("Length of our line: {0:.2f}".format(l_length))

# Get the centroid of the line // Centroid of our line:  POINT (6.229961354035622 -11.892411157572392)
l_centroid = line.centroid
print("Centroid of our line: ", l_centroid)

 # What type is the centroid? // Type of the centroid: <class 'shapely.geometry.point.Point'>
centroid_type = type(l_centroid)
print("Type of the centroid:", centroid_type)


# %%
# 02-3_Polygon

# Create a Polygon from the coordinates
poly = Polygon([(2.2, 4.2), (7.2, -25.1), (9.26, -2.456)])
print(poly)

poly2 = Polygon([[p.x, p.y] for p in [point1, point2, point3]])
print(poly2)

# Geometry type can be accessed as a String // Geometry type as text: Polygon
poly_type = poly.geom_type
print("Geometry type as text:", poly_type)

# Using the Python's type function gives the type in a different format
poly_type2 = type(poly)
print("Geometry how Python shows it:", poly_type2)

world_exterior = [(-180, 90), (-180, -90), (180, -90), (180, 90)]
hole = [[(-170, 80), (-170, -80), (170, -80), (170, 80)]]

# World without a hole
world = Polygon(shell=world_exterior)
print(world)
# // POLYGON ((-180 90, -180 -90, 180 -90, 180 90, -180 90))

world_has_a_hole = Polygon(shell=world_exterior, holes=hole)
print(world_has_a_hole)
# // POLYGON ((-180 90, -180 -90, 180 -90, 180 90, -180 90), (-170 80, -170 -80, 170 -80, 170 80, -170 80))

# Get the centroid of the Polygon
world_centroid = world.centroid
print("Poly centroid: ", world_centroid)
print(type(world_centroid)) # Point

# Get the area of the Polygon
world_area = world.area
print("Poly Area: ", world_area)
print(type(world_area)) # float

# Get the bounds of the Polygon (i.e. bounding box)
world_bbox = world.bounds
print("Poly Bounding Box: ", world_bbox)
print(type(world_bbox)) # tuple

# Get the exterior of the Polygon
world_ext = world.exterior
print("Poly Exterior: ", world_ext)
print(type(world_ext)) # LinearRing

# Get the length of the exterior
world_ext_length = world_ext.length
print("Poly Exterior Length: ", world_ext_length)
print(type(world_ext_length)) # float

# %%
# 02-4_Geometry collections
# Geometric Object & bounding box import
from shapely.geometry import MultiPoint, MultiLineString, MultiPolygon, box

# Create a MultiPoint object of our points 1,2 and 3
multi_point = MultiPoint([point1, point2, point3])
print(multi_point) # MULTIPOINT (2.2 4.2, 7.2 -25.1, 9.26 -2.456)
print(multi_point.geom_type) # MultiPoint

line1 = LineString([point1, point2])
line2 = LineString([point2, point3])
multi_line = MultiLineString([line1, line2])
print("MultiLine: ", multi_line)

# Let's create the exterior of the western part of the world
west_exterior = [(-180, 90), (-180, -90), (0, -90), (0, 90)]

# Let's create a hole --> remember there can be multiple holes, thus we need to have a list of hole(s).
# Here we have just one.
west_hole = [[(-170, 80), (-170, -80), (-10, -80), (-10, 80)]]

# Create Polygon
multi_poly = Polygon(shell=west_exterior, holes=west_hole)
print("MultiPoly: ", multi_poly)

min_x, min_y = 0, -90
max_x, max_y = 180, 90
east_poly_box = box(minx=min_x, miny=min_y, maxx=max_x, maxy=max_y)
print("Bounding box: ", east_poly_box)

# Convex Hull of our MultiPoint --> https://en.wikipedia.org/wiki/Convex_hull

import geopandas as gpd
import matplotlib.pyplot as plt

convex = multi_point.convex_hull
print("Convex hull of the points: ", convex)
mp_plot = gpd.GeoSeries([multi_point])
convex_plot = gpd.GeoSeries([convex])
mp_plot.plot()
convex_plot.plot()
plt.show()

# %%
# ★ len 오류 발생 해결할 필요가 있음 ★
# How many lines do we have inside our MultiLineString?

lines_count = len(multi_line)
print("Number of lines in MultiLineString:", lines_count)

# %%
# Let's calculate the area of our MultiPolygon
multi_poly_area = multi_poly.area
print("Area of our MultiPolygon:", multi_poly_area)
# %%
"""
We can check if we have a "valid" MultiPolygon. MultiPolygon is thought as valid if the individual polygons
does notintersect with each other. Here, because the polygons have a common 0-meridian, we should NOT have
a valid polygon. This can be really useful information when trying to find topological errors from your data
"""
valid = multi_poly.is_valid

print("Is polygon valid?: ", valid)
# %%
