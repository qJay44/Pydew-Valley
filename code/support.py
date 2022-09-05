from os import walk
from pygame.image import load as pg_load_img


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pg_load_img(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

