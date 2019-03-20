import math
from .colorspace import CVC

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
        hsl-dic = {"H": HSLB(0), "S": HSLB(1), "L": HSLB(2), "C": HSLB(5)}
        hsv-dic = {"H": HSLB(0), "S": HSLB(3), "V": HSLB(4), "V": HSLB(5)}
        return {'HSC': hsl-dic, 'HSV': hsv-dic}

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
                if illuminant == "D50 2" :
                    Xn, Yn, Zn = 0.966797, 1.0000, 0.825188
                elif illuminant == "D65 2" :
                    Xn, Yn, Zn = 0.95047, 1.0000, 1.08883
                title = profile + " " + illuminant
                xn, yn = Xn / (Xn + Yn + Zn), Yn / (Xn + Yn + Zn)
                un, vn = 4*xn / (-2*xn + 12*yn + 3), 9*yn / (-2*xn + 12*yn + 3)
                X, Y, Z = self.xyz[profile]["X"], self.xyz[profile]["Y"], self.xyz[profile]["Z"]
                if X+Y+Z == 0:
                    L = 0
                    a, b = 0, 0
                    u, v = 0, 0
                    ua, va = 0, 0
                else :
                    L = (116 * luv_f(Y/Yn) - 16) / 100
                    a, b = (500 * (luv_f(X/Xn) - luv_f(Y/Yn))) / 100, (200 * (luv_f(Y/Yn) - luv_f(Z/Zn))) /100
                    u, v = 4*X / (X + 15*Y + 3*Z), 9*Y / (X + 15*Y + 3*Z)
                    ua, va = 13*L*(u-un), 13*L*(v-vn)
                if abs(a)<0.00001 and abs(b)<0.00001 :
                    H_lab = 0
                elif b<0 :
                    H_lab = math.degrees(math.atan2(b,a)) + 360
                else :
                    H_lab = math.degrees(math.atan2(b,a))
                if abs(ua)<0.00001 and abs(va)<0.00001 :
                    H_luv = 0
                elif va<0 :
                    H_luv = math.degrees(math.atan2(va,ua)) + 360
                else :
                    H_luv = math.degrees(math.atan2(va,ua))
                C_lab = math.sqrt(a*a + b*b)
                C_luv = math.sqrt(ua*ua + va*va)
                if L<0.00001 or L>0.99999 :
                    S_lab = 0
                    S_luv = 0
                else :
                    S_lab = C_lab / L
                    S_luv = C_luv / L
                Lab = {"L":L, "a": a, "b": b, "h": H_lab, "s": S_lab, "c": C_lab}
                Luv = {"L":L, "u": ua, "v": va, "h": H_luv, "s": S_luv, "c": C_luv}    
                Labuv.update({title: {'Lab': Lab, 'Luv': Luv}})
        return Labuv

    def get_group(self, method) :
        group = ''
        if method == 'rgb' :
            if self.rgb['hsl']['l']> 0.9 :
                group = "white"
            elif self.rgb['hsl']['l'] < 0.1 :
                group = "black"
            else :
                if self.rgb['hsl']['c'] < 0.1 :
                    group = "gray"
                else :
                    if self.rgb['hsl']['h'] >= 15 and self.rgb['hsl']['h'] < 45 :
                        if self.rgb['hsl']['l'] >= 0.4 :
                            group = "orange"
                        else :
                            group = "brown"
                    elif self.rgb['hsl']['h'] >= 45 and self.rgb['hsl']['h'] < 75 :
                        group = "yellow"
                    elif self.rgb['hsl']['h'] >= 75 and self.rgb['hsl']['h'] < 105 :
                        if self.rgb['hsl']['l'] >= 0.5 :
                            if self.rgb['hsl']['h'] >= 90 :
                                group = "green"
                            else :
                                group = "yellow"
                        else :
                            group = "green"
                    elif self.rgb['hsl']['h'] >= 105 and self.rgb['hsl']['h'] < 135 :
                        group = "green"
                    elif self.rgb['hsl']['h'] >= 135 and self.rgb['hsl']['h'] < 165 :
                        if self.rgb['hsl']['l'] >= 0.5 :
                            group = "cyan"
                        else :
                            group = "green"
                    elif self.rgb['hsl']['h'] >= 165 and self.rgb['hsl']['h'] < 195 :
                        if self.rgb['hsl']['l'] < 0.5 :
                            if self.rgb['hsl']['h'] >= 180 :
                                group = "blue"
                            else :
                                group = "green"
                        else :
                            group = "cyan"
                    elif self.rgb['hsl']['h'] >= 195 and self.rgb['hsl']['h'] < 225 :
                        if self.rgb['hsl']['l'] >= 0.5 :
                            group = "cyan"
                        else :
                            group = "blue"
                    elif self.rgb['hsl']['h'] >= 225 and self.rgb['hsl']['h'] < 255 :
                        group = "blue"
                    elif self.rgb['hsl']['h'] >= 255 and self.rgb['hsl']['h'] < 285 :
                        if self.rgb['hsl']['l'] >= 0.5 :
                            group = "purple"
                        else :
                            group = "blue"
                    elif self.rgb['hsl']['h'] >= 285 and self.rgb['hsl']['h'] < 315 :
                        if self.rgb['hsl']['l'] < 0.7 :
                            group = "purple"
                        else :
                            group = "pink"
                    elif self.rgb['hsl']['h'] >= 315 and self.rgb['hsl']['h'] < 345 :
                        if self.rgb['hsl']['l'] < 0.7 :
                            if self.rgb['hsl']['h'] >= 330 :
                                group = "red"
                            else :
                                group = "purple"
                        else :
                            group = "pink"
                    
                    else :
                        if self.rgb['hsl']['l'] < 0.7 :
                            group = "red"
                        else :
                            group = "pink"
        return group 

    def get_depth(self, method) :
        depth = ''
        if method == 'rgb' :
            if self.rgb['hsl']['l'] > 0.75 :
                depth = "light"
            elif self.rgb['hsl']['l'] > 0.5 :
                depth = "soft"
            elif self.rgb['hsl']['l'] > 0.25 :
                depth = "deep"
            else :
                depth = "dark"
        return depth

def luv_f(value) :
    delta = 6/29
    if value > delta**3.0 :
        transform = value**(1.0/3.0)
    else :
        transform = value / 3 / (delta**2.0) + 4 / 29
    return transform

def is_hexa(word) :
    hexa=""
    if len(word)==7 and word[0]=="#" :
        hexa = word[1:7]
    elif len(word)==6 :
        hexa = word[0:6]
    else :
        return False
    try:
        int(hexa, 16)
        return hexa
    except ValueError :
        return False

