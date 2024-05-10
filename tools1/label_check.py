import os, json, shutil
import librosa
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
IMG_JSON_PATH = '/internal_img/json/'
DIR = '교량반대방향'
path = DIR + IMG_JSON_PATH
CATEGORY = "A5"
OUT_DIR = f'./result_data/{CATEGORY}/'
IMG_DIR = f'{DIR}/internal_img/img/'
WAV_DIR = f'{DIR}/internal_wav/wav/'
STFT_DIR = f'{DIR}/internal_wav/stft/'
MEL_DIR = f'{DIR}/internal_wav/mel/'
def main():
    file_list = [f for f in os.listdir(path) if f.endswith(".json")]
    file_dict = dict()
    for file in file_list:
        direct = path + file
        with open(direct, 'rb') as jf:
            json_data = json.load(jf)
            label = json_data['image_inside_info']['annotations']
            a = []
            for i in label:
                # if CATEGORY == i['image_label']:
                a.append(i['image_label'])
                    # img_path = OUT_DIR + '/img/' 
                    # shutil.copy(IMG_DIR+file[:13]+"_II.png", img_path+file[:13]+"_II.png")
                    # wav_path = OUT_DIR + '/wav/'
                    # shutil.copy(WAV_DIR+file[:12]+"0_AI.wav", wav_path+file[:12]+"0_AI.wav")
                    # stft_path = OUT_DIR + '/stft/'
                    # shutil.copy(STFT_DIR+file[:12]+"0_AI.png", stft_path+file[:12]+"0_AI.png")
                    # mel_path = OUT_DIR + '/mel/'
                    # shutil.copy(MEL_DIR+file[:12]+"0_AI.png", mel_path+file[:12]+"0_AI.png")
            a = list(set(a))
            name = file[7:12]+"0"
            file_dict[name] = {"img" : a}

    wav_list = [f for f in os.listdir(WAV_DIR) if f.endswith(".wav")]
    for file in wav_list:
        y, sr = librosa.load(WAV_DIR+file, sr=None)
        n_fft =2048
        D = np.abs(librosa.stft(y))
        S = librosa.feature.melspectrogram(S=D, sr=sr, n_fft=n_fft, hop_length=512, n_mels=64)
        mel_spect = librosa.power_to_db(S, ref=np.max)
        count = 0
        mel_spect[mel_spect <= np.mean(mel_spect)+1.7] = mel_spect.min()
        for num, i in enumerate(mel_spect):
            if num < 8:
                mel_spect[num] = mel_spect.min()
            elif num > 12 and num < 28:
                mel_spect[num] = mel_spect.min()
            elif num > 38:
                mel_spect[num] = mel_spect.min()
        for num, i in enumerate(mel_spect):
            slice = int(len(i)*0.2)
            _i = sorted(i)[slice:-slice]
            mean = sum(_i)/len(_i)
            if mean > mel_spect.min()+1.7:
                count += 1
        name = file[7:12]+"0"
        if count > 8:
            file_dict[name]['audio'] = "A"
        else:
            file_dict[name]['audio'] = "N"
        
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    j = 2
    sheet['A1'] = "index"
    sheet['B1'] = 'img_label'
    sheet['C1'] = 'audio_label'

    for key, value in file_dict.items():
        sheet[f'A{j}'] = key
        sheet[f'B{j}'] = str(value['img'])
        sheet[f'C{j}'] = str(value['audio'])
        j += 1
    sheet['E1'] = "Img Label"
    sheet["F1"] = "Count"
    sheet["G1"] = "Audio N"
    sheet["H1"] = "Audio A"
    for i in range(1,6):
        sheet[f'E{i+1}'] = f'A{i}'
        sheet[f'F{i+1}'] = f'=COUNTIF(B2:B{j},"*A{i}*")'
        sheet[f'G{i+1}'] = f'=COUNTIFS(C2:C{j},"N",B2:B{j},"*A{i}*")'
        sheet[f'H{i+1}'] = f'=COUNTIFS(C2:C{j},"A",B2:B{j},"*A{i}*")'
    

    workbook.save('label.xlsx')
    workbook.close()

if __name__ == "__main__":
    main()
