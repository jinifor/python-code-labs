import pickle
import json
from pathlib import Path
from typing import List, Dict, Any, Union
from shapely.geometry import Polygon, MultiPolygon, mapping
import geojson
from datetime import datetime
import numpy as np

# Class to convert PKL files to GeoJSON
class PKLToGeoJSON:
    def __init__(self, input_file: str):
        """
        PKL 파일을 GeoJSON으로 변환하는 클래스 초기화

        Args:
            input_file (str): 입력 PKL 파일 경로
        """
        self.input_file = Path(input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

    def read_pkl_file(self) -> List[Union[Polygon, MultiPolygon]]:
        """
        PKL 파일을 읽어서 Shapely Polygon/MultiPolygon 리스트로 반환 (0번 인덱스 제외)
        - 0번 인덱스는 지점이라 제외함

        Returns:
            List[Union[Polygon, MultiPolygon]]: Shapely Polygon/MultiPolygon 객체 리스트
        """
        try:
            print(f"Reading file: {self.input_file}")
            with open(self.input_file, 'rb') as f:
                try:
                    data = pickle.load(f)
                    print(f"Loaded data type: {type(data)}")
                    print(f"Data content: {data}")
                except Exception as e:
                    print(f"Pickle loading error: {str(e)}")
                    raise
                
            if not isinstance(data, list):
                raise ValueError(f"PKL file must contain a list of polygons, got {type(data)}")
            
            # 0번 인덱스를 제외한 데이터만 사용 (지점이라 제외)
            if len(data) > 1:
                data = data[1:]
            else:
                raise ValueError("No data available after skipping first item")
            
            # 각 항목을 Polygon 또는 MultiPolygon으로 변환
            converted_data = []
            for i, item in enumerate(data):
                if isinstance(item, (Polygon, MultiPolygon)):
                    converted_data.append(item)
                else:
                    raise ValueError(f"Item {i} is neither a Shapely Polygon nor MultiPolygon, got {type(item)}")
                    
            return converted_data
            
        except pickle.UnpicklingError as e:
            print(f"Unpickling error details: {str(e)}")
            raise ValueError("Invalid PKL file format")
        except Exception as e:
            print(f"Error reading PKL file: {str(e)}")
            raise

    def convert_to_geojson(self, geometries: List[Union[Polygon, MultiPolygon]]) -> Dict[str, Any]:
        """
        Polygon/MultiPolygon 리스트를 GeoJSON 형식으로 변환
        
        Args:
            geometries (List[Union[Polygon, MultiPolygon]]): Shapely geometry 객체 리스트
            
        Returns:
            Dict[str, Any]: GeoJSON 형식의 딕셔너리
        """
        features = []
        
        for i, geometry in enumerate(geometries):
            try:
                if geometry.is_empty:
                    print(f"Warning: Geometry {i} is empty, skipping...")
                    continue

                # Geometry를 GeoJSON 형식으로 변환
                geometry_dict = mapping(geometry)
                
                # 면적과 길이 계산
                try:
                    area = geometry.area
                    perimeter = geometry.length
                except Exception as e:
                    print(f"Warning: Failed to calculate area/length for geometry {i}: {str(e)}")
                    area = 0
                    perimeter = 0

                # Feature 생성
                feature = geojson.Feature(
                    geometry=geometry_dict,
                    properties={
                        "id": i,
                        "timestamp": datetime.now().isoformat(),
                        "area": area,
                        "perimeter": perimeter
                    }
                )
                features.append(feature)

            except Exception as e:
                print(f"Warning: Failed to process geometry {i}: {str(e)}")
                continue
        
        if not features:
            raise ValueError("No valid features after processing all geometries")

        # FeatureCollection 생성 (CRS 정보 포함)
        feature_collection = geojson.FeatureCollection(
            features,
            crs={
                "type": "name",
                "properties": {
                    "name": "EPSG:5179"
                }
            }
        )
        return feature_collection

    def save_geojson(self, geojson_data: Dict[str, Any], output_file: str) -> None:
        """
        GeoJSON 데이터를 파일로 저장
        
        Args:
            geojson_data (Dict[str, Any]): GeoJSON 형식의 딕셔너리
            output_file (str): 출력 파일 경로
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, ensure_ascii=False, separators=(',', ':'))

    def convert(self, output_file: str) -> None:
        """
        PKL 파일을 GeoJSON으로 변환하고 저장
        
        Args:
            output_file (str): 출력 GeoJSON 파일 경로
        """
        # PKL 파일 읽기
        geometries = self.read_pkl_file()
        
        # GeoJSON으로 변환
        geojson_data = self.convert_to_geojson(geometries)
        
        # 파일로 저장
        self.save_geojson(geojson_data, output_file)

def main():
    """
    명령행에서 실행될 때 사용되는 메인 함수
    """
    import argparse

    parser = argparse.ArgumentParser(description='Convert PKL file to GeoJSON')
    parser.add_argument('input_file', help='Input PKL file path')
    parser.add_argument('output_file', help='Output GeoJSON file path')

    args = parser.parse_args()
    
    try:
        converter = PKLToGeoJSON(args.input_file)
        converter.convert(args.output_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
