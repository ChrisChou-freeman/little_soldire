import os
from enum import Enum, auto

from pygame import image, surface

def listdir_clean(path: str) -> list[str]:
   files = os.listdir(path)
   files = sorted(files)
   return list(filter(lambda x:x!='.DS_Store', files))

def pygame_load_images_list(path: str) -> list[surface.Surface]:
    file_list = listdir_clean(path)
    return [ image.load(os.path.join(path, file)) for file in file_list]

def pygame_load_iamges_with_name(path: str) -> dict[str, surface.Surface]:
    folder_name = path.split('/')[-1]
    file_list = listdir_clean(path)
    return {f'{folder_name}_{file}': image.load(os.path.join(path, file)) for file in file_list}

