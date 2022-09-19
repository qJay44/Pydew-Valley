from os import walk
from pygame.image import load as pg_load_img


def import_folder(path):
    surface_list = []

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg_load_img(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for _, _, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg_load_img(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict

