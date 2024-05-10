import os, json
'''
    특정 폴더의 json 파일속의 데이터를 수정하기 위해 사용.
    img 측에서 잘못된 라벨링 데이터명을 사용하여 해당 부분을 수정하기 위해 사용.
'''
# 디렉토리 경로
directory = 'C:/Users/elan5/OneDrive/바탕 화면/JEJU_JSON/내부 이미지'

# 디렉토리 내 모든 파일 목록 가져오기
for filename in os.listdir(directory):
    if filename.endswith(".json"):  # JSON 파일만 처리
        file_path = os.path.join(directory, filename)
        
        # JSON 파일 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # JSON 데이터에서 원하는 부분 수정
            data['pipe_info']['pipe_id'] = "JEJU_B"
            data['data_info']['data_id'] = filename[:13]
            data['image_inside_info']['image_file_name'] = filename[:13] +"_II.png"

        # 수정된 JSON 데이터 파일로 저장
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)