import shutil, os, random

path = 'external/교량방향/'
file_list = [f for f in os.listdir(path) if f.endswith(".wav")]

for i in range(0,20):
    rand = random.randint(0,224)
    file_path = path + file_list[rand]
    file_name, old_extension = os.path.splitext(os.path.basename(file_path))
    out_path = path + file_name + f"_{i}.wav"
    print(file_path, out_path)
    shutil.copy(file_path, out_path)