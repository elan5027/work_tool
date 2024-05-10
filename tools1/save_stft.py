

import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import os
import argparse
'''
    특정 폴더를 입력받아 해당 폴더의 wav 폴더안의 wav파일을 찾아 해당 파일을
    특정 폴더의 stft 폴더에 stft 파일로 변환하여 저장하기 위한 스크립트.
'''

def change_path(in_file, out_folder, extension):

    file_name, old_extension = os.path.splitext(os.path.basename(in_file))
    new_file_name = file_name + extension
    new_file_path = os.path.join(out_folder, new_file_name)
    return new_file_path


def save_stft(in_file, out_folder):
    y, sr = librosa.load(in_file, sr=None)
    
    fig, ax = plt.subplots()
    
    D = librosa.power_to_db(np.abs(librosa.stft(y)), ref=np.max)  # 최대치를 데시벨 변환 기준값 (0 DB) 설정하여 변환
    img = librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')

    plt.tight_layout(pad=0)     
        # Save only the image without any white spaces or borders
    os.makedirs(out_folder, exist_ok=True)
    out_file = change_path(in_file, out_folder, '.png')
    fig.colorbar(img, ax=ax, format="%+2.0f dB")  #데시벨 바 출력, 최대치를 0으로하고 음수값으로 색상표시
    plt.savefig(out_file, bbox_inches='tight', pad_inches=0, format='png')    
    plt.close()

    return out_file

def main():

    parser = argparse.ArgumentParser(description="WAV to STFT file into segments.")
    parser.add_argument("directory_path", help="Input file path")
    args = parser.parse_args()
    path = os.path.join(args.directory_path, 'ttest2')
    file_list = [f for f in os.listdir(path) if f.endswith(".wav")]

    # 파일 목록 출력
    for file in file_list:
        direct = os.path.join(args.directory_path, "ttest2", file)
        out_file = save_stft(direct, os.path.join(args.directory_path,'stft'))
        print(out_file)

if __name__ == "__main__":
    main()
