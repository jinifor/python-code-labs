# pkl파일을 읽고 출력하는 프로그램

import pickle

def read_pkl_file(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def main():
    """
    명령행에서 실행될 때 사용되는 메인 함수
    """
    import argparse

    parser = argparse.ArgumentParser(description='Convert PKL file to GeoJSON')
    parser.add_argument('input_file', help='Input PKL file path')

    args = parser.parse_args()
    
    try:
        data = read_pkl_file(args.input_file)
        print(data)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
