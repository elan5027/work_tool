import argparse, os
import scipy.signal
import scipy.io.wavfile as wavfile

parser = argparse.ArgumentParser(description="Split a WAV file into segments.")
parser.add_argument("directory_path", help="Input file path")
args = parser.parse_args()
path = args.directory_path + '/'
file_list = [f for f in os.listdir(path) if f.endswith(".wav")]

for file in file_list:
    direct = args.directory_path +"/"+ file
    out_folder = args.directory_path+'/'+'modify/'
    
    # wav 파일 로드
    sample_rate, audio_data = wavfile.read(direct)

    # 노이즈 제거를 위한 윈도우 크기 설정 (조정 가능)
    #window_size = 91
    window_size = 301

    # 중앙값 필터링을 사용하여 노이즈 제거
    smoothed_audio = scipy.signal.medfilt(audio_data, kernel_size=window_size)

    # 결과를 새로운 wav 파일로 저장
    wavfile.write(out_folder+file, sample_rate, smoothed_audio)
    print(file)


