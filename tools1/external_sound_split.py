import argparse
import librosa
import soundfile as sf
import os, wave, json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

'''
    특정 폴더를 입력받아 해당 폴더의 wav 폴더안의 wav파일을 찾아 해당 파일을
    특정 시간단위로 잘라내어 wav 폴더에 저장하며, json 폴더에 json 데이터를 저장한다.
    입력값 :
        1. 잘라낼 오디오 파일
        2. 해당 파일의 분류번호 (1-9)
        3. 내부, 외부 음향 (AI, AO)
        4. 음향을 자를 시작 시간 (초) | 지정하지 않을 경우 0초로 지정
        5. 저장할 폴더 경로  |  지정하지 않을 경우 output_dir 폴더로 지정
        6. 자를 시간 단위 (초)  | 지정하지 않을 경우 5초로 설정
'''

TIME_UNIT = 2
TYPE_JSON = 'json'
TYPE_WAV = 'wav'
SEGMENT = 10
#4번 교량반대 상 1-1 시작시간
TIME = {
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
    "audio_outside_label": "N"
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
        'length(s)': round(duration_seconds,3)
    }

    return wav_info

def save_wav(in_file, out_folder):   

    # WAV 파일 읽기
    sample_rate, data = wavfile.read(in_file)
    
    # WAV 파일의 시간 축 생성
    time = np.arange(0, len(data)) / sample_rate
    
    # 파형 시각화
    plt.figure(figsize=(10, 4))
    plt.plot(time, data)
    plt.title('WAV File Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    out_file = change_path(in_file, out_folder, '.png')
    plt.savefig(out_file)    
    plt.close()    
    return out_file

def save_json(path, wavefile, start, end, number):
    ai_info = get_wav_param(wavefile)
    _start_time = TIME[number]+timedelta(seconds=start-3)
    
    _end_time = TIME[number]+timedelta(seconds=end-3)
    _start = f'{_start_time.strftime("%Y%m%d %H:%M:%S")}'
    _end = f'{_end_time.strftime("%Y%m%d %H:%M:%S")}'
    
    side = "outside"
    info = ex_info
    info[f'audio_{side}_id'] = ai_info['file_path'][-20:-4]
    info[f'audio_{side}_file_name'] = ai_info['file_path'][-20:]
    info[f'audio_{side}_original_file_name'] = f"JEJU_B_{str(number)}.{TYPE_WAV}"
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
    print(f"Saved WAV File path :  {json_file}")


def main():
    parser = argparse.ArgumentParser(description="Split a WAV file into segments.")
    parser.add_argument("input_dir", help="Input directory")
    parser.add_argument("--start_time", type=float, default=0, help="Start time (in seconds)")
    parser.add_argument("--output_dir", default="output_files", help="Output directory")
    
    args = parser.parse_args()
    out_dir = os.path.join(args.output_dir, TYPE_WAV)
    os.makedirs(out_dir, exist_ok=True)

    set_duration = 5

    _start_time = start_time = 0
    _end_time = end_time = 5
    wav_path = args.input_dir+"/"
    wav_files = [filename for filename in os.listdir(wav_path) if filename.endswith(".wav")]

    # files_to_rename_as_down = 900
    # files_to_rename_as_up_1 = 165
    # files_to_rename_as_up_2 = 618
    # j=0
    # k=0
    # index = 0
    # for i, filename in enumerate(wav_files):
    #     check_index = index
    #     if i < files_to_rename_as_down:
    #         num = 400020 + (i*10)
    #         index = 4
            
    #     elif i < files_to_rename_as_down + files_to_rename_as_up_1:
    #         num = 500020 + (j*10)
    #         j+=1
    #         index = 5
    #     else:
    #         num = 600020 + (k*10)
    #         k+=1
    #         index = 6
    #     if index != check_index:
    #         _start_time = 0
    #         _end_time = 5

    num = 700000
    index = 7
    for filename in wav_files:

        #new_filename = f"JEJU_B_{str(num)}_AO.{TYPE_WAV}"
        y, sr = librosa.load(wav_path+filename, sr=None, offset=start_time, duration=set_duration)
        output_file = os.path.join(out_dir, filename)
        print(output_file)
        sf.write(output_file, y, sr)
        print(f'''======================================\nSaved WAV File path :  {output_file}''')
        # save_wav(args.output_dir+f'/{TYPE_WAV}/'+filename, args.output_dir+'/'+'wavinfo')
        # save_json(args.output_dir, output_file, _start_time, _end_time, index)
        _start_time = _start_time+2 
        _end_time = _end_time+2 
        print(f'''Duration : {set_duration} \nStart time : {start_time} \nEnd time :  {end_time}\n======================================\n
        ''')
        num = num + 10
        
if __name__ == "__main__":
    main()
