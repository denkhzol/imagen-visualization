import numpy as np


def calculate_2d_distance(x1, x2, y1, y2):
    return np.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


def obtain_image_path(file_number, image_folder):
    image_file = str(file_number).zfill(6) + '.png'
    image_path = image_folder / image_file
    return image_path
