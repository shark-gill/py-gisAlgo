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
$ conda install -c conda-forge gdal
$ gdal-config --version
```
- package mng
```bash
$ pip freeze > requirements.txt # 패키지 확인
$ pip install -r requirements.txt # 패키지 설치
```

## Source
> 1) GIS Algorithm DOI: https://github.com/gisalgsf
> 2) GDAL Install DOI: https://opensourceoptions.com/blog/how-to-install-gdal-with-anaconda/