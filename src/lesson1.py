#%%
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
from shapely.geometry import Point


point1 = Point(2.2, 4.2)
print(point1)

# %%
