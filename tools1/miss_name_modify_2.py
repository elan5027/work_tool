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

directory_path = "external/교량반대방향/wav/"  # 디렉토리 경로를 지정하세요
new_prefix = 153161
endwich = '.wav'
time = datetime(year=2023, month=10, day=8, hour=16, minute=3, second=49)
#1007171520
settime = time

file_list = os.listdir(directory_path)


for file_name in file_list:
    print(type(file_name))
    if "N" in file_name:
        mask = "N"
    else :
        mask = "L"
    
    print(file_name)
    sec = random.randint(12,37)
    file_time = f'{settime.strftime("%Y%m%d_%H_%M_%S")}'
    if os.path.isfile(os.path.join(directory_path, file_name)): 
        new_file_name = f'{str(new_prefix)}_{file_time}_126_{mask}.png'
        # 새로운 파일 이름으로 파일 이름 변경
        os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_file_name))
        new_prefix = new_prefix + 1
        settime = settime+timedelta(seconds=sec)
        print(settime)
    