# GIS Algorithm

## 의존성(Dependency)
- Python 3.8.16
- conda 22.9.0
```bash
$ conda create -n {venv name}
$ conda --version
```
- GDAL 3.6.3
```bash
$ conda install -c conda-forge gdal # 패키지 설치 시 환경 확인 필요
$ gdal-config --version
```
- package mng
```bash
$ pip freeze > requirements.txt # 패키지 확인
$ pip install -r requirements.txt # 패키지 설치
```
- shapely 2.0.1
```bash
$ conda update --all
$ conda install shapely --channel conda-forge
```

## Source
> 1) GIS Algorithm DOI: https://github.com/gisalgsf
> 2) GDAL Install DOI: https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/
> 3) [BASE] GIS Algorithm DOI: https://geo-python-site.readthedocs.io/en/latest/
> 4) [HARD] GIS Algorithm DOI: https://automating-gis-processes.github.io/2017/lessons/L7/network-analysis.html
> 4) Python을 활용한 빅데이터와 데이터 과학 DOI: http://bigdata.dongguk.ac.kr/lectures/datascience/_book/index.html
> 5) Python 모듈을 활용한 공간 분석 DOI: https://www.inflearn.com/course/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%AA%A8%EB%93%88%ED%99%9C%EC%9A%A9-%EA%B3%B5%EA%B0%84%EB%B6%84%EC%84%9D#curriculum