import os, re
import argparse
from datetime import datetime, timedelta
import random
'''
    파일이름을 변환하는 스크립트.
    음향 데이터의 이름 라벨링이 잘못되었을때 해당 부분을 수정하기 위하여 작성.
    Ex. JEJU_A_100000_AI 이름을 JEJU_B_100000_AI 형식으로 폴더단위로 일괄 수정하기 위해 사용.
'''
parser = argparse.ArgumentParser(description="Modify Filename into segments.")
parser.add_argument("in_path", help="in file path")
parser.add_argument("out_path", help="out file path")
args = parser.parse_args()

directory_path = "C:/Users/elan5/OneDrive/바탕 화면/JEJU_FILE/내부 음향/modi"  # 디렉토리 경로를 지정하세요
to = "C:/Users/elan5/OneDrive/바탕 화면/JEJU_FILE/내부 음향"
# 디렉토리 내의 파일 목록 가져오기
file_list = os.listdir(directory_path)

# 파일이름을 정렬하기 위해 사용

for file_name in file_list:
    
    if os.path.isfile(os.path.join(directory_path, file_name)): 
        name_number_map=f'{file_name[:12]}0_AI.wav'
        print(name_number_map)
        os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, name_number_map))
    