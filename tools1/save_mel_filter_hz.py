

import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
import os
import argparse, json
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
    

    os.makedirs(out_folder, exist_ok=True)
    out_file = change_path(in_file, out_folder, '.png')
    plt.tight_layout(pad=0)     
    
    ax.set(title='Mel-frequency spectrogram')
    count = 0
    
    # 이미지의 평균값을 가져와서 평균값보다 낮은 주파수 대역은 최소 데시벨로 설정하여 검정색으로 처리한다.
    # 이떄 단순 평균값은 평균화된 이미지에서 잘못된 값을 가져 올 수 있기 떄문에 POWER 값으로 평균값보다 다소 높은 수치로 필터한다.
    FILTER_POWER = 1.7
    
    mel_spect[mel_spect <= mel_spect.mean()+FILTER_POWER] = mel_spect.min()
    
    for num, i in enumerate(mel_spect):
        if num < 8:
            mel_spect[num] = mel_spect.min()
        elif num > 12 and num < 30:
            mel_spect[num] = mel_spect.min()
        elif num > 37:
            mel_spect[num] = mel_spect.min()
    mel = np.sort(mel_spect, axis=1)
    for i, _mel in enumerate(mel):
        # 해당 리스트의 평균값이 최소값의 특정치 보다 높을 경우 비정상 음향으로 판단한다.
        # 가장 우측의 값 10%는 잡소음의 영역이라 가정하고 이미지의 평균값으로 치환한다.
        index = int(_mel.size*0.9)
        mel[i][index:] = mel_spect.min()
    for i in mel:
        if i.mean() > mel_spect.min()+FILTER_POWER:
            count += 1
    if count > 8:
        img = librosa.display.specshow(mel, y_axis='mel', sr=sr, ax=ax)
        fig.colorbar(img, ax=ax, format="%+2.0f dB")
        plt.savefig(out_file, bbox_inches='tight', pad_inches=0, format='png') 
        # JSON_PATH = 'C:/Users/elan5/OneDrive/바탕 화면/JEJU_JSON/내부 음향'
        # json_file = out_file = change_path(in_file, JSON_PATH, '.json')
        # with open(json_file, 'r', encoding='utf-8') as file:
        #     data = json.load(file)
        #     data['audio_inside_label'] = 'A'
           
    plt.close()

    return out_file

def main():

    parser = argparse.ArgumentParser(description="WAV to STFT file into segments.")
    parser.add_argument("directory_path", help="Input file path")
    args = parser.parse_args()
    path = args.directory_path
    file_list = [f for f in os.listdir(path) if f.endswith(".wav")]

    # 파일 목록 출력
    for file in file_list:
        direct = os.path.join(args.directory_path, file)
        out_file = save_mel(direct, os.path.join(args.directory_path,'result'))
        print(out_file)

if __name__ == "__main__":
    main()
