# KPG to GeoJSON Converter

KPG (Pickle) 파일을 GeoJSON 형식으로 변환하는 Python 모듈입니다.

## 환경 설정

### Conda 환경 생성 및 활성화

```bash
# Conda 환경 생성 (Python 3.11 버전 사용)
conda create -n labs-pickle-geojson python=3.11

# 환경 활성화
conda activate labs-pickle-geojson

# conda-forge 채널 추가
conda config --add channels conda-forge
```

### 필요한 패키지 설치

```bash
# 기본 패키지 설치
conda install shapely geojson numpy

# 또는 requirements.txt를 사용하여 설치
pip install -r requirements.txt
```

## 사용 방법

### 명령행에서 실행

```bash
# 환경이 활성화된 상태에서
python kpg_to_geojson.py input.kpg output.geojson
```

### Python 코드에서 사용

```python
from kpg_to_geojson import KPGToGeoJSON

# 변환기 초기화
converter = KPGToGeoJSON("input.kpg")

# 변환 실행
converter.convert("output.geojson")
```

## 기능

- KPG (Pickle) 파일에서 Shapely Polygon 객체 리스트 읽기
- Polygon 객체를 GeoJSON 형식으로 변환
- 각 Polygon에 대한 메타데이터 포함 (ID, 타임스탬프, 면적, 둘레)
- UTF-8 인코딩으로 GeoJSON 파일 저장

## 환경 요구사항

- Miniconda 또는 Anaconda
- Python 3.11
- shapely
- geojson
- numpy

## 문제 해결

### 일반적인 문제

1. **패키지 설치 오류**
   ```bash
   # conda-forge 채널 추가 후 다시 시도
   conda config --add channels conda-forge
   conda install shapely geojson numpy
   ```

2. **Python 버전 문제**
   ```bash
   # Python 버전 확인
   python --version
   
   # 필요한 경우 다른 버전으로 환경 재생성
   conda create -n labs-pickle-geojson python=3.10
   ```

## 라이선스

MIT License