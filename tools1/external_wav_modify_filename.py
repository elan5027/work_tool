import os
'''
    외부 음향데이터의 이름을 일괄 변경하기 위해 사용. 
    데이터의 각 갯수를 지정하여 인덱스 번호로 나누어 작성.
'''
# 디렉토리 경로
directory = './external/교량반대방향/wav/'

# 디렉토리 내 모든 .wav 파일 목록 가져오기
wav_files = [filename for filename in os.listdir(directory) if filename.endswith(".wav")]

# A로 변경할 파일 수와 B로 변경할 파일 수 설정
files_to_rename_as_down = 900
files_to_rename_as_up_1 = 165
files_to_rename_as_up_2 = 618
j=0
k=0
for i, filename in enumerate(wav_files):
    if i < files_to_rename_as_down:
        num = 400020 + (i*10)
        new_filename = "JEJU_B_"+ str(num) + "_AO.wav"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
    elif i < files_to_rename_as_down + files_to_rename_as_up_1:
        num = 500020 + (j*10)
        new_filename = "JEJU_B_" + str(num) + "_AO.wav"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        j+=1
    else:
        num = 600020 + (k*10)
        new_filename = "JEJU_B_" + str(num) + "_AO.wav"
        os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        k+=1