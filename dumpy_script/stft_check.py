import librosa
import matplotlib.pyplot as plt

wav_file_path = "교량방향/internal_wav/wav/JEJU_B_705360_AI.wav"
signal, sample_rate = librosa.load(wav_file_path)

import numpy as np

def stft(signal, window_size, hop_length):
    n_frames = 1 + (len(signal) - window_size) // hop_length
    stft_matrix = np.empty((window_size // 2 + 1, n_frames))
    
    for i in range(n_frames):
        frame = signal[i * hop_length: i * hop_length + window_size]
        windowed_frame = frame * np.hamming(window_size)
        stft_matrix[:, i] = np.fft.rfft(windowed_frame)

    return stft_matrix

window_size = 1024
hop_length = 512
stft_matrix = stft(signal, window_size, hop_length)

def plot_spectrogram(stft_matrix, sample_rate, hop_length):
    magnitude_spectrogram = np.abs(stft_matrix)
    print(sample_rate)
    log_spectrogram = librosa.amplitude_to_db(magnitude_spectrogram)
    plt.figure()
    librosa.display.specshow(log_spectrogram, sr=sample_rate, hop_length=hop_length, x_axis="time", y_axis="linear")
    
    plt.colorbar(format="%+2.0f dB")
    plt.title("Spectrogram")
    plt.show()

plot_spectrogram(stft_matrix, sample_rate, hop_length)

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.io import wavfile
# from scipy.signal import spectrogram


# # WAV 파일을 읽어옵니다.
# sample_rate, x = wavfile.read(wav_file_path)

# # 스펙트로그램 매개변수 설정
# NFFT = 512  # FFT 포인트 수
# noverlap = 3   # 겹치는 부분

# # 스펙트로그램 계산
# frequencies, times, Sxx = spectrogram(x, fs=sample_rate, nperseg=NFFT, noverlap=noverlap, nfft=NFFT)

# # 스펙트로그램 그리기
# plt.figure()
# plt.pcolormesh(times, frequencies, 10 * np.log10(np.abs(Sxx)), shading='auto')
# plt.title('Spectrogram')
# plt.xlabel('Time (s)')
# plt.ylabel('Frequency (Hz)')
# plt.colorbar()

# plt.show()


