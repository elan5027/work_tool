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
#set_time = 

#5번 교량반대 상 1-2 시작시간
#set_time = 

#6번 교량반대 하 시작시간
#set_time = 

#7번 교량방향 시작시간
#set_time = 

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

in_info = {
    "audio_inside_id": "",
    "audio_inside_file_name": "",
    "audio_inside_num_channels": "",
    "audio_inside_sample_width": "",
    "audio_inside_frame_rate": "",
    "audio_inside_num_frames": "",
    "audio_inside_length": 5.0,
    "audio_inside_timestamp_start": "",
    "audio_inside_timestamp_end": "",
    "audio_inside_label": "N"
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

def save_json(path, index, wavefile, start, end, type, number):
    ai_info = get_wav_param(wavefile)
    _start_time = TIME[number]+timedelta(seconds=start)
    
    _end_time = TIME[number]+timedelta(seconds=end)
    _start = f'{_start_time.strftime("%Y%m%d %H:%M:%S")}'
    _end = f'{_end_time.strftime("%Y%m%d %H:%M:%S")}'
    if "AI" == type:
        side = "inside"
        info = in_info
        
    else :
        side = "outside"
        info = ex_info
    
    info[f'audio_{side}_id'] = ai_info['file_path'][-20:-4]
    info[f'audio_{side}_file_name'] = ai_info['file_path'][-20:]
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
    parser.add_argument("input_file", help="Input WAV file")
    parser.add_argument("start_index", choices=range(1, 9), type=int, default=1, help="Starting index number")
    parser.add_argument("location", choices=["AI", "AO"], help="Choose between Internal(AI) or external(AO)")
    parser.add_argument("--start_time", type=float, default=0, help="Start time (in seconds)")
    parser.add_argument("--output_dir", default="output_files", help="Output directory")
    parser.add_argument("--duration", type=float, default=5.0, help="Duration of each segment (in seconds)")
    
    args = parser.parse_args()
    out_dir = os.path.join(args.output_dir, TYPE_WAV)
    os.makedirs(out_dir, exist_ok=True)

    segment_index = (args.start_index * 100000)
    set_duration = args.duration
    half_duration = set_duration / 2

    start_time = 0 if (args.start_time - half_duration) < 0 else (args.start_time - half_duration)
    end_time = half_duration + args.start_time
    current = args.start_time
    end_duration = librosa.get_duration(path=args.input_file)

    counter = 1
    is_exit = False

    #for _ in range(1,20):
    while True:
        
        if current < half_duration:
            set_duration = end_time - start_time
        elif current + half_duration >= end_duration:  
            set_duration =  end_duration -start_time
            end_time = end_duration
            is_exit = True
        else:
            set_duration = args.duration

        y, sr = librosa.load(args.input_file, sr=None, offset=start_time, duration=set_duration)
        filename = f"JEJU_B_{segment_index}_{args.location}.{TYPE_WAV}"
        output_file = os.path.join(out_dir, filename)
        
        #노이즈 제거 검증 후 추가 예정

        sf.write(output_file, y, sr)
        print(f'''======================================\nCount : {counter}\nCurrent : {current}\nSaved WAV File path :  {output_file}''')
        #save_wav(args.output_dir+f'/{TYPE_WAV}/'+filename, args.output_dir+'/'+'wavinfo')
        save_json(args.output_dir, args.start_index, output_file, start_time, end_time, args.location, args.start_index)

        print(f'''Duration : {set_duration} \nStart time : {start_time} \nEnd time :  {end_time}\n======================================\n
        ''')

        if is_exit:
            print(f"\n\nTotal : {counter}")
            break

        current += TIME_UNIT
        start_time = 0 if (current - half_duration) < 0 else current - half_duration
        segment_index += SEGMENT
        end_time = current + half_duration
        
        counter += 1
        
if __name__ == "__main__":
    main()
