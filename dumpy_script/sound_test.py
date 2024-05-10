import numpy as np
from scipy.io import wavfile
from scipy.signal import spectrogram
from sklearn.ensemble import IsolationForest
import os
import librosa, math

num = {1,2,3,4}
path = "./교량방향/internal_wav/noise_wav/"
#path = "./classes/crack/wav/"

file_list = [f for f in os.listdir(path) if f.endswith(".wav")]
        # 파일 목록 출력
for file in file_list:
    # 오디오 파일 경로 설정
#audio_path = "./classes/crack/wav/audio_1.wav"
#audio_path = "./교량방향/internal_wav/wav/JEJU_B_700080_AI.wav"
# 오디오 파일을 읽어옵니다.
    audio, sampla_rate = librosa.load(path+file, sr=None)
    # 스펙트로그램 매개변수 설정
    nperseg = 2048  # FFT 크기
    noverlap = 1024  # 겹치는 부분
    # 스펙트로그램 계산
    frequencies, times, Sxx = spectrogram(audio, fs=sampla_rate, nperseg=nperseg, noverlap=noverlap)
    # 스펙트로그램 데이터를 이상 탐지 모델에 적용
    # 여기에서는 Isolation Forest를 사용하여 이상을 탐지하는 예시를 보여줍니다.
    model = IsolationForest(contamination=0.15)  # 5% 이상 데이터를 이상으로 판단
    X = np.log(np.abs(Sxx).T)  # 스펙트로그램 데이터에 로그를 취함

    # spectrogram = librosa.feature.melspectrogram(y=audio, sr=sampla_rate, n_fft=nperseg, hop_length=noverlap)
    # frequencies = librosa.core.mel_frequencies(n_mels=spectrogram.shape[0], fmin=0, fmax=sampla_rate/2)
    # times = librosa.frames_to_time(range(spectrogram.shape[1]), sr=sampla_rate, hop_length=noverlap)
    # Sxx = librosa.power_to_db(spectrogram, ref=np.max)
    # X = Sxx.T
    predictions = model.fit_predict(X)

    # 이상으로 판단된 시간대 출력
    abnormal_times = times[predictions == -1]
    check = []
    
    for a in abnormal_times:
        check.append(math.ceil(a))
    check_set = set(check)
    
    if num.issuperset(check_set):
        print("이상으로 판단된 시간대:", file, num)