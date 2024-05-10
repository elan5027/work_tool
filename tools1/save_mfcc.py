

import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import os
import argparse
'''
    특정 폴더를 입력받아 해당 폴더의 wav 폴더안의 wav파일을 찾아 해당 파일을
    특정 폴더의 mel 폴더에 mel spectogram 파일로 변환하여 저장하기 위한 스크립트.
'''

def change_path(in_file, out_folder, extension):

    file_name, old_extension = os.path.splitext(os.path.basename(in_file))
    new_file_name = file_name + extension
    new_file_path = os.path.join(out_folder, new_file_name)
    return new_file_path


def save_mel(in_file, out_folder):
    y, sr = librosa.load(in_file, sr=None)
    D = np.abs(librosa.stft(y))
    mfcc = librosa.core.power_to_db((librosa.feature.mfcc(y=y, sr=sr)), ref=np.max)
    fig, ax = plt.subplots(figsize=(15,9))
    img = librosa.display.specshow(mfcc, x_axis='time',
                            y_axis='mel', sr=sr, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='MFCCs')
    os.makedirs(out_folder, exist_ok=True)
    out_file = change_path(in_file, out_folder, '.png')
    plt.savefig(out_file, bbox_inches='tight', pad_inches=0, format='png')    

    return out_file

def main():

    parser = argparse.ArgumentParser(description="WAV to STFT file into segments.")
    parser.add_argument("directory_path", help="Input file path")
    args = parser.parse_args()
    path = os.path.join(args.directory_path, 'wav')
    file_list = [f for f in os.listdir(path) if f.endswith(".wav")]

    # 파일 목록 출력
    for file in file_list:
        direct = os.path.join(args.directory_path, "wav", file)
        out_file = save_mel(direct, os.path.join(args.directory_path,'test'))
        print(out_file)

if __name__ == "__main__":
    main()
