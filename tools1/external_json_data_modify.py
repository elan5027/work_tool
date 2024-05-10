import os, json
from datetime import datetime, timedelta
'''
    특정 폴더의 json 파일속의 데이터를 수정하기 위해 사용.
    img 측에서 잘못된 라벨링 데이터명을 사용하여 해당 부분을 수정하기 위해 사용.
'''
# 디렉토리 경로
DIR = '2'
directory = f'./{DIR}/internal_img/json/'

# 디렉토리 내 모든 파일 목록 가져오기
for filename in os.listdir(directory):
    #print(filename)
    if filename.endswith(".json"):  # JSON 파일만 처리
        file_name, old_extension = os.path.splitext(os.path.basename(filename))
        file_path = os.path.join(directory, filename)
        
        # JSON 파일 열기
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # JSON 데이터에서 원하는 부분 수정
            settime = data['data_info']['detection_time']
            
            modify_name = file_name[0:-1]+'0_AO.json'
            print(modify_name)
            modify_path = os.path.join("교량방향", 'external_wav', 'json', '2', modify_name)
            time = datetime(int(settime[:4]), int(settime[4:6]), int(settime[6:8]), int(settime[9:11]), int(settime[12:14]), int(settime[15:17]))
            start = time+timedelta(seconds=-3)
            end = time+timedelta(seconds=2)
            _start = f'{start.strftime("%Y%m%d %H:%M:%S")}'
            _end = f'{end.strftime("%Y%m%d %H:%M:%S")}'
            # 수정된 JSON 데이터 파일로 저장
            with open(modify_path, 'r', encoding='utf-8') as modify_file:
                modify_data = json.load(modify_file)
                modify_data['audio_outside_timestamp_start'] = _start
                modify_data['audio_outside_timestamp_end'] = _end
                
                with open(modify_path, 'w', encoding='utf-8') as modify_file2:
                    
                    print(_start, _end)
                    json.dump(modify_data, modify_file2, indent=4)