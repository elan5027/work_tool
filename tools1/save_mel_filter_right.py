

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
    n_fft =2048
    fig, ax = plt.subplots()
    # mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=n_fft, hop_length=512, n_mels=64)
    # mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    # img = librosa.display.specshow(mel_spect, x_axis='time', y_axis='mel')
    #     # Save only the image without any white spaces or borders


    D = np.abs(librosa.stft(y))
    S = librosa.feature.melspectrogram(S=D, sr=sr, n_fft=n_fft, hop_length=512, n_mels=64)
    mel_spect = librosa.power_to_db(S, ref=np.max)
    #img = librosa.display.specshow(mel_spect, x_axis='time', y_axis='mel', sr=sr, ax=ax)

    os.makedirs(out_folder, exist_ok=True)
    out_file = change_path(in_file, out_folder, '.png')
    plt.tight_layout(pad=0)     
    #fig.colorbar(img, ax=ax, format="%+2.0f dB")
    ax.set(title='Mel-frequency spectrogram')
    count = 0
    mel_spect2 = librosa.power_to_db(S, ref=np.max)
    mel_spect[mel_spect <= np.mean(mel_spect)+1.7] = mel_spect.min()
    mel = np.sort(mel_spect, axis=1)
    for num, i in enumerate(mel_spect):
        if num > 8:
            mel_spect[num] = mel_spect.min()
        elif num > 12 and num < 28:
            mel_spect[
                num] = mel_spect.min()
        elif num > 38:
            mel_spect[num] = mel_spect.min()
    for num, i in enumerate(mel_spect):
        slice = int(len(i)*0.3)
        mel[num][slice:-slice]
        if mel.mean() > mel_spect.min()+1.7:
            count += 1
    # #if count > 8:
    # for num, i in enumerate(mel_spect2):
    #     mel_spect2[num] = sorted(i)
        
    img = librosa.display.specshow(mel_spect, x_axis='time', y_axis='mel', sr=sr, ax=ax)
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    plt.savefig(out_file, bbox_inches='tight', pad_inches=0, format='png')    
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
        direct = os.path.join(args.directory_path, "wav", file)
        out_file = save_mel(direct, os.path.join(args.directory_path,'test4'))
        print(out_file)

if __name__ == "__main__":
    main()
