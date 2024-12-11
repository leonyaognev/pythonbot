import os
from natsort import natsorted


def rename(file_name):
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/files/")
    for serial in os.listdir('files'):
        serial = serial.replace(" ", '''\ ''')
        os.system(
            f'mv ~/Documents/pythonbot/files/{serial} ~/Documents/pythonbot/files/{file_name}')
        for index, seson in enumerate(natsorted(os.listdir(f'files/{file_name}'))):
            seson = seson.replace(' ', '\ ')
            os.system(f'find ~/Documents/pythonbot/files/{file_name}/{
                      seson} ' + '-mindepth 1 -type d -exec rm -rf {} +')
            for i, s in enumerate(natsorted(os.listdir(f'files/{file_name}/{seson.replace("\ ", " ")}'))):
                print(s)
                extention = s.split('.')[-1]
                s = s.replace(" ", '''\ ''')
                os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{seson}/{
                    s} ~/Documents/pythonbot/files/{file_name}/{seson}/{file_name}_{index+1}_{i+1}.mp4')
            os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{
                      seson} ~/Documents/pythonbot/files/{file_name}/{
                      index+1}')
