from PIL import Image
import os

def make_result(n: int, name: str):
    img = Image.open('./screenshots/00.png')
    file_list = sorted(os.listdir('./screenshots'),)
    result_img = Image.new('RGB', (img.width, img.height*n))
    for idx, file in enumerate(file_list):
        img = Image.open(f'screenshots/{file}')
        result_img.paste(img, (0, idx*img.height))
    result_width = result_img.width  // 2
    result_img = result_img.crop((0, 0, result_width, result_img.height))
    result_img.save(f'result/{name}.jpg', optimize=True, quality=95)

def init():
    clean('./result')
    clean('./screenshots')

def clean(filepath):
    if os.path.exists(filepath):
        for file in os.scandir(filepath):
            os.remove(file.path)
        os.removedirs(filepath)
    os.mkdir(filepath)
