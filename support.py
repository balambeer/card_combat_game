import pygame as pg
from os import walk

def import_folder(path):
    img_list = []
    for _,_,img_files in walk(path):
        for img in img_files:
            image_surf = pg.image.load(path + "/" + img).convert_alpha()
            img_list.append(image_surf)
    return img_list

def slide_distortion(t, a):
    if t < 0:
        0
    elif t < 0.5:
        0.5 * a * t * a * t
    elif t < 1:
        1 - 0.5 * a * (1 - t) * a * (1 - t)
    else:
        1

class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y