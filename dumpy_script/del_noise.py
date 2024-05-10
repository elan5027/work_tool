import librosa
import numpy as np
import argparse, os
import soundfile as sf

def denoise_audio(audio_path, output_path):
    # 오디오 파일 불러오기
    audio, sr = librosa.load(audio_path, sr=None)
    
    # 스펙트로그램 계산
    spectrogram = np.abs(librosa.stft(audio))
    
    # 스펙트로그램을 기반으로 노이즈 마스크 생성
    noise_mask = np.mean(spectrogram, axis=1) < 0.01
    
    # 노이즈 마스크를 이용하여 스펙트로그램 수정
    denoised_spectrogram = spectrogram.copy()
    denoised_spectrogram[noise_mask] = 0
    
    # 수정된 스펙트로그램을 이용하여 음성 데이터 복원
    denoised_audio = librosa.istft(denoised_spectrogram)
    print()
    # 복원된 음성 데이터 저장
    #librosa.output.write_wav(output_path, denoised_audio, sr)
    sf.write(output_path, denoised_audio, sr)


def main():
    parser = argparse.ArgumentParser(description="WAV to STFT file into segments.")
    parser.add_argument("directory_path", help="Input file path")
    args = parser.parse_args()
    path = args.directory_path + '/wav/'
    file_list = [f for f in os.listdir(path) if f.endswith(".wav")]
    # 파일 목록 출력
    for file in file_list:
        denoise_audio(path+file, args.directory_path+'/noise_wav/'+file)
    #denoise_audio("s.wav", "_s.wav")
if __name__ == "__main__":
    main()