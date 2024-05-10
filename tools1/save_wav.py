import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.io import wavfile

'''
    특정 폴더를 입력받아 해당 폴더의 wav 폴더안의 wav파일을 찾아 해당 파일을
    특정 폴더의 waveinfo 폴더에 wav 이미지 파일로 변환하여 저장하기 위한 스크립트.
'''

TYPE_WAV = 'wav'

def change_path(in_file, out_folder, extension):

    file_name, old_extension = os.path.splitext(os.path.basename(in_file))
    new_file_name = file_name + extension
    new_file_path = os.path.join(out_folder, new_file_name)
    return new_file_path

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
    print(out_file)
    plt.savefig(out_file)    
    plt.close()    
    return out_file

def main():
    parser = argparse.ArgumentParser(description="WAV to STFT file into segments.")
    parser.add_argument("directory_path", help="Input file path")
    args = parser.parse_args()
    path = os.path.join(args.directory_path, 'wav')
    file_list = [f for f in os.listdir(path) if f.endswith(".wav")]
    # 파일 목록 출력
    for file in file_list:
        save_wav(os.path.join(path+file), os.path.join(args.directory_path, 'wavinfo'))

if __name__ == "__main__":
    main()