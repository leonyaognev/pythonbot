import os
from natsort import natsorted
import ffmpeg


shielding = [' ', "'", '"', '|', '&', ';', '>', '<', '*', '?', '[', ']',
             '(', ')', '{', '}', '$', '#', '~', '=', '%', '!', '/', ':']


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


async def rename_many_seasons(file_name):
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/downloads/")
    for serial in os.listdir('downloads'):
        serial = serial.replace('\\', '\\\\')
        for i in shielding:
            serial = serial.replace(i, '\\'+i)
        os.system(
            f'mv ~/Documents/pythonbot/downloads/{serial}\
                    ~/Documents/pythonbot/downloads/{file_name}')
        for index, seson in enumerate(natsorted(os.listdir(
            f'downloads/{file_name}'))
        ):
            seson = seson.replace('\\', '\\\\')
            for i in shielding:
                seson = seson.replace(i, '\\'+i)
            os.system(f'find ~/Documents/pythonbot/downloads/{file_name}/{
                      seson} ' + '-mindepth 1 -type d -exec rm -rf {} +')
            os.system(f'mv ~/Documents/pythonbot/downloads//{file_name}/{
                      seson} ~/Documents/pythonbot/downloads/{file_name}/{
                      index+1}')
            for i, s in enumerate(natsorted(os.listdir(
                f'downloads/{file_name}/{index+1}'))
            ):
                s = s.replace('\\', '\\\\')
                for item in shielding:
                    s = s.replace(item, '\\' + item)
                extention = s.split('.')[-1]
                os.system(
                    f'mv ~/Documents/pythonbot/downloads/{file_name}/{
                        index+1}/{s} ~/Documents/pythonbot/downloads/{
                        file_name}/{index+1}/{file_name}_{index+1}_{i+1}.{
                        extention}'
                )
                print(
                    f'mv ~/Documents/pythonbot/downloads/{file_name}/{
                        index+1}/{s} ~/Documents/pythonbot/downloads/{
                        file_name}/{index+1}/{file_name}_{index+1}_{i+1}.{
                        extention}'
                )
                convert_to_mp4(
                    f'/home/ognev/Documents/pythonbot/downloads/{file_name}/{
                        index+1}/{file_name}_{index+1}_{i+1}.{extention}',
                    f'/home/ognev/Documents/pythonbot/downloads/{
                        file_name}/{index+1}/{file_name}_{index+1}_{i+1}.mp4'
                )
    os.system(
        "mv ~/Documents/pythonbot/downloads/* ~/Documents/pythonbot/files/")


async def rename_one_season(file_name):
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/downloads/")
    seas = file_name.split()[0]
    file_name = file_name.split()[1]
    for serial in os.listdir('downloads'):
        serial = serial.replace('\\', '\\\\')
        for i in shielding:
            serial = serial.replace(i, '\\'+i)
        os.system(
            f'mv ~/Documents/pythonbot/downloads/{serial}\
                    ~/Documents/pythonbot/downloads/{file_name}')
        print(
            f'mv ~/Documents/pythonbot/downloads/{serial}\
                    ~/Documents/pythonbot/downloads/{file_name}')
        os.system(f'find ~/Documents/pythonbot/downloads/{
                  file_name} ' + '-mindepth 1 -type d -exec rm -rf {} +')
        os.system(f'mkdir ~/Documents/pythonbot/downloads/{file_name}/1/')
        os.system(
            f'mv ~/Documents/pythonbot/downloads/{file_name}/*\
                ~/Documents/pythonbot/downloads/{file_name}/1/'
        )
        for index, seson in enumerate(natsorted(os.listdir(
            f'downloads/{file_name}'))
        ):
            seson = seson.replace('\\', '\\\\')
            for i in shielding:
                seson = seson.replace(i, '\\'+i)
            os.system(
                f'find ~/Documents/pythonbot/downloads/{file_name}/{
                    seson} ' + '-mindepth 1 -type d -exec rm -rf {} +'
            )
            os.system(
                f'mv ~/Documents/pythonbot/downloads//{file_name}/{
                    seson} ~/Documents/pythonbot/downloads/{file_name}/{seas}'
            )
            for i, s in enumerate(natsorted(os.listdir(
                f'downloads/{file_name}/{seas}'))
            ):
                s = s.replace('\\', '\\\\')
                for item in shielding:
                    s = s.replace(item, '\\'+item)
                extention = s.split('.')[-1]
                os.system(
                    f'mv ~/Documents/pythonbot/downloads/{
                        file_name}/{seas}/{
                        s} ~/Documents/pythonbot/downloads/{file_name}/{
                        seas}/{file_name}_{seas}_{i+1}.{extention}')
                convert_to_mp4(
                    f'/home/ognev/Documents/pythonbot/downloads/{file_name}/{
                        seas}/{file_name}_{seas}_{i+1}.{extention}',
                    f'/home/ognev/Documents/pythonbot/downloads/{
                        file_name}/{seas}/{file_name}_{seas}_{i+1}.mp4'
                )
    os.system("mv ~/Documents/pythonbot/downloads/*\
            ~/Documents/pythonbot/files/")
