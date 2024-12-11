import os
from natsort import natsorted
import ffmpeg


def convert_to_mp4(input_file, output_file):
    try:
        ffmpeg.input(input_file).output(output_file,
                                        vcodec='libx264',
                                        acodec='aac').run(
            overwrite_output=True
        )
        os.system(f'rm -rf {input_file}')
        print(f"Файл успешно конвертирован: {output_file}")
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")


def rename(file_name):
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/downloads/")
    for serial in os.listdir('downloads'):
        serial = serial.replace(' ', '\ ')
        os.system(
            f'mv ~/Documents/pythonbot/downloads/{serial} ~/Documents/pythonbot/downloads//{file_name}')
        for index, seson in enumerate(natsorted(os.listdir(f'downloads/{file_name}'))):
            seson = seson.replace(' ', '\ ')
            os.system(f'find ~/Documents/pythonbot/downloads/{file_name}/{
                      seson} ' + '-mindepth 1 -type d -exec rm -rf {} +')
            os.system(f'mv ~/Documents/pythonbot/downloads//{file_name}/{
                      seson} ~/Documents/pythonbot/downloads/{file_name}/{
                      index+1}')
            for i, s in enumerate(natsorted(os.listdir(f'downloads/{file_name}/{index+1}'))):
                print(s)
                s = s.replace(' ', '\ ')
                extention = s.split('.')[-1]
                os.system(f'mv ~/Documents/pythonbot/downloads/{file_name}/{index+1}/{
                    s} ~/Documents/pythonbot/downloads/{file_name}/{index+1}/{file_name}_{index+1}_{i+1}.{extention}')
                convert_to_mp4(
                    f'/home/ognev/Documents/pythonbot/downloads/{file_name}/{
                        index+1}/{file_name}_{index+1}_{i+1}.{extention}',
                    f'/home/ognev/Documents/pythonbot/downloads/{
                        file_name}/{index+1}/{file_name}_{index+1}_{i+1}.mp4'
                )
    os.system("mv ~/Documents/pythonbot/downloads/* ~/Documents/pythonbot/files/")


rename('мужик-один-удар')
