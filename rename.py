import os


def rename(file_name):
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/files/")
    for serial in os.listdir('files'):
        os.system(
            f'mv ~/Documents/pythonbot/files/{serial} \
                    ~/Documents/pythonbot/files/{file_name}')
        for index, seson in enumerate(sorted(os.listdir(f'files/{file_name}'))):
            for i, s in enumerate(sorted(os.listdir(f'files/{file_name}/{seson}'))):
                os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{seson}/{
                    s} ~/Documents/pythonbot/files/{file_name}/{seson}/{file_name}_{index+1}_{i+1}.mp4')
            os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{
                      seson} ~/Documents/pythonbot/files/{file_name}/{
                      index+1}')
