import os
import pickle

from pygame import image, surface

from .common_type import WorldDataStruct

def listdir_clean(path: str) -> list[str]:
   files = os.listdir(path)
   files = sorted(files)
   return list(filter(lambda x:x!='.DS_Store', files))

def pygame_load_images_list(path: str) -> list[surface.Surface]:
    file_list = listdir_clean(path)
    return [ image.load(os.path.join(path, file)) for file in file_list]

def pygame_load_iamges_with_name(path: str) -> dict[str, surface.Surface]:
    file_list = listdir_clean(path)
    return { file: image.load(os.path.join(path, file)) for file in file_list  }

def load_world_data(world_data_path: str) -> WorldDataStruct:
    with open(world_data_path, 'rb') as file_obj:
        world_data_obj: WorldDataStruct = pickle.load(file_obj)
        return world_data_obj

def write_world_data(
        world_data_path: str,
        world_data_obj: WorldDataStruct) -> None:
    with open(world_data_path, 'wb') as  file_obj:
        pickle.dump(world_data_obj, file_obj)
