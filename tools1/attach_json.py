import re
import argparse
import os, json
'''
    IMG Json, internal Json, external json 각 3개의 json 파일을 통합하기 위해 사용.
'''
INTERNAL_IMG_PATH = "JEJU_JSON/내부 이미지/"
INTERNAL_WAV_PATH = "JEJU_JSON/내부 음향/"
EXTERNAL_WAV_PATH = "JEJU_JSON/외부 음향/"
ONE_JSON_PATH = "JEJU_JSON/one_json_label"

def mach_json(in_file, path):
    wav_file_match = re.search(r'\d+', in_file)
    wav_number = int(wav_file_match.group()[:-1])
    total_dict = dict()
    img_list = [f for f in os.listdir(INTERNAL_IMG_PATH) if f.endswith(".json")]
    for file in img_list:
        file_match = re.search(r'\d+', file)
        json_number = int(file_match.group()[:-1])
        if wav_number == json_number:
            with open(INTERNAL_IMG_PATH+file, 'r') as img_json:
                img_dict = json.load(img_json)
                total_dict = img_dict
            with open(INTERNAL_WAV_PATH+in_file[:12]+"0_AI.json", 'r') as ai_json:
                ai_dict = json.load(ai_json)
                total_dict['audio_inside_info'] = ai_dict
            with open(EXTERNAL_WAV_PATH+in_file[:12]+"0_AO.json", 'r') as ao_json:
                ao_dict = json.load(ao_json)
                total_dict['audio_outside_info'] = ao_dict
            out_folder = os.path.join(path, ONE_JSON_PATH)
            total_file = os.path.join(out_folder, in_file[:12]+"0.json")
            with open(path+total_file, 'w', encoding='utf-8') as f:
                json.dump(total_dict, f, indent = 4, ensure_ascii=False)
    # for i, file in enumerate(file_list):
    #     file_match = re.search(r'\d+', file)
    #     json_number = int(file_match.group()[:-1])
    #     if wav_number == json_number:
    #         with open(total_json_path+file, 'r') as json_file:
    #             data_dict = json.load(json_file)
    #             with open(path+INTERNAL_WAV_PATH+file, 'r') as in_json_file:
    #                 internal_dict = json.load(in_json_file)
    #                 data_dict['audio_inside_info'] = internal_dict
    #                 json_name = in_file[:12]+"0_AO.json"
    #             try:
    #                 with open(path+EXTERNAL_WAV_PATH+json_name, 'r') as ex_json_file:
                        
    #                     external_dict = json.load(ex_json_file)
    #                     data_dict['audio_outside_info'] = external_dict
    #                     out_folder = os.path.join(path, ONE_JSON_PATH)
    #                     json_file2 = os.path.join(out_folder, file)
                        
    #                     with open(path+json_file2, 'w', encoding='utf-8') as f:
    #                         json.dump(data_dict, f, indent = 4, ensure_ascii=False)
                            
    #             except FileNotFoundError:
    #                 pass
    


def main():
    parser = argparse.ArgumentParser(description="Total Json into segments.")
    parser.add_argument("directory_path", help="Input file path")
    # input = "교량방향"
    args = parser.parse_args()
    path = args.directory_path + INTERNAL_WAV_PATH
    file_list = [f for f in os.listdir(path) if f.endswith(".json")]
    count = 0
    # 파일 목록 출력
    for file in file_list:
        #files = args.directory_path +INTERNAL_WAV_PATH+ file
        mach_json(file, args.directory_path)
        count += 1
    print(count)
if __name__ == "__main__":
    main()
