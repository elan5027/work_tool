import librosa, os
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

path = "./leak_data/wav/"
#path = "./classes/normal_pipe/wav/"

file_list = [f for f in os.listdir(path) if f.endswith(".wav")]
        # 파일 목록 출력
for file in file_list:
    y, sr = librosa.load(path+file)
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
    # Convert to log scale (dB). We'll use the peak power as reference.
    log_S = librosa.logamplitude(S, ref_power=np.max)
    

    # Make a new figure
    plt.figure(figsize=(12,4))

    # Display the spectrogram on a mel scale
    # sample rate and hop length parameters are used to render the time axis
    librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')

    # Put a descriptive title on the plot
    plt.title('mel power spectrogram')

    # draw a color bar
    plt.colorbar(format='%+02.0f dB')

    # Make the figure layout compact
    plt.tight_layout()