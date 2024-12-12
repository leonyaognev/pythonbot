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
    os.system("mv ~/Downloads/downloads/* ~/Documents/pythonbot/files/")
    for serial in os.listdir('files'):
        serial = serial.replace(' ', '\ ')
        os.system(
            f'mv ~/Documents/pythonbot/files/{serial} ~/Documents/pythonbot/files/{file_name}')
        for index, seson in enumerate(natsorted(os.listdir(f'files/{file_name}'))):
            seson = seson.replace(' ', '\ ')
            os.system(f'find ~/Documents/pythonbot/files/{file_name}/{
                      seson} ' + '-mindepth 1 -type d -exec rm -rf {} +')
            for i, s in enumerate(natsorted(os.listdir(f'files/{file_name}/{seson.replace("\ ", " ")}'))):
                print(s)
                s = s.replace(' ', '\ ')
                os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{seson}/{
                    s} ~/Documents/pythonbot/files/{file_name}/{seson}/{file_name}_{index+1}_{i+1}.mp4')
            os.system(f'mv ~/Documents/pythonbot/files/{file_name}/{
                      seson} ~/Documents/pythonbot/files/{file_name}/{
                      index+1}')
