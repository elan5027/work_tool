import librosa, os
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

path = "./classes/Scale/wav/"
#path = "./classes/normal_pipe/wav/"

file_list = [f for f in os.listdir(path) if f.endswith(".wav")]
        # 파일 목록 출력
for file in file_list:
    y, sr = librosa.load(path+file)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=200)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(librosa.power_to_db(mfccs, ref=np.max), y_axis='mel', x_axis='time')
    plt.colorbar(format='%+2.0f dB')
    plt.title('MFCC')
    path1, _ = os.path.splitext(os.path.basename(file))
    print(path)
    plt.savefig("./classes/Scale/mfcc/"+path1+'.png', bbox_inches='tight', pad_inches=0, format='png')    
    plt.close()
    # zcr = librosa.feature.zero_crossing_rate(y)

    # plt.figure(figsize=(10, 6))
    # plt.title('제로 크로스 레이트 (ZCR)')
    # plt.xlabel('시간 (s)')
    # plt.ylabel('진폭')
    # plt.plot(zcr[0], color='r', label='ZCR')
    # plt.legend()
    # plt.grid()
    # plt.show()