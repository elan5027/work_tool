import os, re
import argparse
'''
    파일이름을 변환하는 스크립트.
    음향 데이터의 이름 라벨링이 잘못되었을때 해당 부분을 수정하기 위하여 작성.
    Ex. JEJU_A_100000_AI 이름을 JEJU_B_100000_AI 형식으로 폴더단위로 일괄 수정하기 위해 사용.
'''
parser = argparse.ArgumentParser(description="Modify Filename into segments.")
parser.add_argument("in_path", help="in file path")
parser.add_argument("out_path", help="out file path")
parser.add_argument("index", help="file index number")
args = parser.parse_args()

directory_path = "1/internal_wav/json/"  # 디렉토리 경로를 지정하세요
new_prefix = "JEJU_B_"  # 새로운 접두사를 지정하세요
end_prefix = ".json"

# 디렉토리 내의 파일 목록 가져오기
file_list = os.listdir(directory_path)

# 파일이름을 정렬하기 위해 사용
name_number_map = {}
for i, file_name in enumerate(file_list):
    if os.path.isfile(os.path.join(directory_path, file_name)):  # 파일인 경우에만 처리
        # 파일 이름에서 숫자를 추출 (정규 표현식 사용)
        match = re.search(r'(\d+)', file_name)
        if match:
            number = int(match.group())  # 정수로 변환
            
            name_number_map[file_name] = number
        # 새로운 파일 이름 생성 (여기에서는 접두사를 추가하는 예시)
        new_file_name = new_prefix + str(number) + end_prefix
        
        # 새로운 파일 이름으로 파일 이름 변경
        os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_file_name))
        
      

# 숫자를 기준으로 파일 이름 정렬

# sorted_files = sorted(name_number_map.keys(), key=lambda x: name_number_map[x])
# # numberling = int(args.index) * 100000
# for file_name in sorted_files:
    
    
#     if os.path.isfile(os.path.join(directory_path, file_name)):  # 파일인 경우에만 처리
#         # 새로운 파일 이름 생성 (여기에서는 접두사를 추가하는 예시)
#         new_file_name = new_prefix + str(number) + end_prefix
        
#         # 새로운 파일 이름으로 파일 이름 변경
#         #os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_file_name))
#         print(file_name, new_file_name)
#     # numberling+=10