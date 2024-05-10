import os, json, shutil
IMG_JSON_PATH = '/internal_wav/test/'
DIR = '교량반대방향'
path = DIR + IMG_JSON_PATH
IMG_PATH = DIR + '/internal_img/img/'
OUT_DIR = f'./bridge_annormal/'
def main():
    file_list = [f for f in os.listdir(path) if f.endswith(".png")]
    for file in file_list:
        img_list = [f for f in os.listdir(IMG_PATH) if f.endswith(".png")]
        for img in img_list:
            if file[:12] == img[:12]:
                shutil.copy(IMG_PATH+img, OUT_DIR)
            
                    

if __name__ == "__main__":
    main()
