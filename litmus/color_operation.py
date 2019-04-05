import math
from .color_space import CVC
# Two Color Operation

class CVO():
    @staticmethod
    def distance_rgb(hexa1, hexa2):
        rgb1 = CVC.hexa_rgb(hexa1)
        rgb2 = CVC.hexa_rgb(hexa2)
        del_r = abs(rgb2[0]-rgb1[0])
        del_g = abs(rgb2[1]-rgb1[1])
        del_b = abs(rgb2[2]-rgb1[2])
        distance = math.sqrt(del_r*del_r + del_g*del_g + del_b*del_b)
        return distance
    