import argparse
import re
import os, wave, json
from datetime import datetime, timedelta

'''
    외부 음향 파일을 JSON 형태로 추출 하기 위해 사용.
    
'''

TYPE_JSON = 'json'
TYPE_WAV = 'wav'
TIME = {
    1:datetime(year=2023, month=10, day=7, hour=14, minute=36, second=57),
    2:datetime(year=2023, month=10, day=7, hour=15, minute=51, second=10),
    3:datetime(year=2023, month=10, day=7, hour=17, minute=41, second=9),
    4:datetime(year=2023, month=10, day=8, hour=17, minute=41, second=3),
    5:datetime(year=2023, month=10, day=8, hour=18, minute=11, second=4),
    6:datetime(year=2023, month=10, day=8, hour=16, minute=9, second=32),
    7:datetime(year=2023, month=10, day=8, hour=15, minute=36, second=14)
}

ex_info = {
    "audio_outside_id": "",
    "audio_outside_file_name": "",
    "audio_outside_original_file_name": "",
    "audio_outside_num_channels": "",
    "audio_outside_sample_width": "",
    "audio_outside_frame_rate": "",
    "audio_outside_num_frames": "",
    "audio_outside_length": 5.0,
    "audio_outside_timestamp_start": "",
    "audio_outside_timestamp_end": "",
    "audio_outside_label": ""
}

def change_path(in_file, out_folder, extension):

    file_name, old_extension = os.path.splitext(os.path.basename(in_file))
    new_file_name = file_name + extension
    new_file_path = os.path.join(out_folder, new_file_name)
    return new_file_path

def get_wav_param(in_file):
    
    with wave.open(in_file, 'rb') as wav_file:
        num_channels, sample_width, frame_rate, num_frames, _, _ = wav_file.getparams()
    # WAV 파일의 길이 계산 (초)
    duration_seconds = num_frames / frame_rate
    wav_info = {
        'file_path': in_file,
        'num_channels': num_channels,
        'sample_width': sample_width,
        'frame_rate': frame_rate,
        'num_frames': num_frames,
        'length(s)': round(duration_seconds,1)
    }

    return wav_info

def save_json(path, index, wavefile, start, end, type, number):
    ai_info = get_wav_param(wavefile)
    _start_time = TIME[number]+timedelta(seconds=start)
    _end_time = TIME[number]+timedelta(seconds=end)
    _start = f'{_start_time.strftime("%Y%m%d %H:%M:%S")}'
    _end = f'{_end_time.strftime("%Y%m%d %H:%M:%S")}'
    if number == 5:
        print(_start_time, _end_time)
    side = "outside"
    info = ex_info
    
    info[f'audio_{side}_id'] = ai_info['file_path'][-20:-4]
    info[f'audio_{side}_file_name'] = ai_info['file_path'][-20:]
    info[f'audio_{side}_original_file_name'] = f"JEJU_B_{str(index)}.{TYPE_WAV}"
    info[f'audio_{side}_num_channels'] = ai_info['num_channels']
    info[f'audio_{side}_sample_width'] = ai_info['sample_width']
    info[f'audio_{side}_frame_rate'] = ai_info['frame_rate']
    info[f'audio_{side}_length'] = ai_info['length(s)']
    info[f'audio_{side}_num_frames'] = ai_info['num_frames']
    info[f'audio_{side}_timestamp_start'] = _start
    info[f'audio_{side}_timestamp_end'] = _end
    info[f'audio_{side}_label'] = "N"
    # json 파일로 저장
    out_folder = os.path.join(path, TYPE_JSON)
    json_name = f'{info[f"audio_{side}_id"]}.{TYPE_JSON}'
    json_file = os.path.join(out_folder, json_name)
    os.makedirs(out_folder, exist_ok=True)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent = 4, ensure_ascii=False)
    #print(f"Saved WAV File path :  {json_file}")


def main():
    parser = argparse.ArgumentParser(description="Total Json into segments.")
    parser.add_argument("directory_path", help="Input file path")
    # input = "교량방향"
    args = parser.parse_args()
    path = args.directory_path + '/external_wav/' 
    file_list = [f for f in os.listdir(path+'wav/미정/') if f.endswith(".wav")]
    start = 1
    end = 6
    print(file_list, path)
    # 파일 목록 출력
    number = 0
    for file in file_list:
        direct = path + 'wav/미정/' + file
        file_match = re.search(r'\d+', file)
        
        json_number = int(file_match.group()[0])
        if number != json_number:
            start = 1
            end = 6
            number = json_number
        #print(json_number)
        save_json(path, json_number, direct, start, end, "AO", number=json_number)
        start+=2
        end+=2
if __name__ == "__main__":
    main()
