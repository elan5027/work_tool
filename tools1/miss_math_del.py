import os, re
'''
    파일이름을 변환하는 스크립트.
    음향 데이터의 이름 라벨링이 잘못되었을때 해당 부분을 수정하기 위하여 작성.
    Ex. JEJU_A_100000_AI 이름을 JEJU_B_100000_AI 형식으로 폴더단위로 일괄 수정하기 위해 사용.
'''

directory_path = "./JEJU_FILE/내부 이미지/"  # 디렉토리 경로를 지정하세요

# 디렉토리 내의 파일 목록 가져오기
file_list = os.listdir(directory_path)

# 파일이름을 정렬하기 위해 사용
name_number_map = []
for file_name in file_list:
    if os.path.isfile(os.path.join(directory_path, file_name)):  # 파일인 경우에만 처리
        # 파일 이름에서 숫자를 추출 (정규 표현식 사용)
        match = re.search(r'(\d+)', file_name)
        if match:
            number = str(match.group())  
            if number[0] == '7':
                name_number_map.append(number[0:5])
count = 0
wav_dir = "./JEJU_FILE/내부 음향/7/"
file_list = os.listdir(wav_dir)
for file_name in file_list:
    match = re.search(r'(\d+)', file_name)
    if match:
        number = str(match.group())[0:5]  # 정수로 변환
    if os.path.isfile(os.path.join(wav_dir, file_name)):
        if number not in name_number_map:   
            count += 1 
            os.remove(wav_dir+file_name)
            print(file_name, number)
        