import math
from .color_space import CVC

class ColorVector():
    def __init__(self, hexa) :
        self.profile = ["sRGB", "Adobe RGB", "CIE RGB"]
        self.illuminant = ["D50 2", "D65 2"]
        self.hexa = hexa
        self.rgb = CVC.hexa_rgb(hexa)
        self.RGB=  self.get_RGB()
        self.HSLV =  self.get_HSLV()
        self.CMYK =  self.get_CMYK()
        self.XYZ =  self.get_XYZ()
        self.Labuv =  self.get_labuv()
        self.group = self.get_group('rgb')
        self.depth = self.get_depth('rgb')
        
    def get_RGB(self) :
        # from hexa to RGB & rgb
        RGB = CVC.hexa_RGB(self.hexa)
        rgb = self.rgb
        RGB_dic = {"R": RGB[0], "G":RGB[1], "b":RGB[2]}
        rgb_dic = {"r":rgb[0], "g":rgb[1], "b":rgb[2]}
        # from RGB to RGB parameters
        param = CVC.RGB_parameters(RGB)
        param_dic = {"Sum":param[0], "Max":param[1], "Min":param[2], "Sigma":param[3], "Delta":param[4]}
        # from rgb to HSL(rgb)
        HSL = CVC.rgb_HSLrgb(rgb)
        HSL_dic = {"H": HSL[0], "S": HSL[1], "L":HSL[2], "C": HSL[3]}
        # from rgb to GEOrgb
        geo = CVC.rgb_GEOrgb(rgb)
        GEO_dic = {"Long": geo[0], "Lati": geo[1], "Radius": geo[2]}
        return {"RGB": RGB_dic, "rgb": rgb_dic, "Parameters": param_dic, "HSL(rgb)": HSL_dic, "GEO(rgb)": GEO_dic}

    def get_HSLV(self) :
        HSLV = CVC.rgb_HSLV(self.rgb)
        hsl-dic = {"H": HSLV(0), "S": HSLV(1), "L": HSLV(2), "C": HSLV(5)}
        hsv-dic = {"H": HSLV(0), "S": HSLV(3), "V": HSLV(4), "C": HSLV(5)}
        return {'HSL': hsl-dic, 'HSV': hsv-dic}

    def get_CMYK(self) :
        CMYK = CVC.rgb_CMYK(self.rgb)
        return {"C": CMYK[0], "M": CMYK[1], "Y": CMYK[2], "K": CMYK[3]}

    def get_XYZ(self) :
        XYZ = {}
        for profile in self.profile:
            xyz = rgb_XYZ(self.rgb, profile)
            xyz-dic = {"X": XYZ[0], "Y": XYZ[1], "Z": XYZ[2], "L": XYZ[3], "x": XYZ[4], "y": XYZ[5]}
            XYZ.update({profile: xyz-dic})
        return XYZ

    def get_Labuv(self) :
        Labuv = {}
        for profile in self.profile :
            for illuminant in self.illuminant :
                title = profile + " " + illuminant
                XYZ = rgb_XYZ(self.rgb, profile)
                L= CVC.XYZ_Labuv(XYZ, illuminant)
                Lab = {"L":L[0], "a": L[1], "b": L[1], "H": L[3], "S": L[4], "C": L[6]}
                Luv = {"L":L[0], "u": L[0], "v": L[7], "H": L[8], "S": L[9], "C": L[10]}    
                Labuv.update({title: {'Lab': Lab, 'Luv': Luv}})
        return Labuv

    def get_group(self, method) :
        if method == 'rgb' :
            group = CVC.rgb_group(self.rgb)
        return group 

    def get_depth(self, method) :
        if method == 'rgb' :
            depth = CVC.rgb_depth(self.rgb)
        return depth



