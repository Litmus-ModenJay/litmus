import math

class ColorVector():
    def __init__(self, hexa) :
        self.profile = ["sRGB", "Adobe RGB", "CIE RGB"]
        self.illuminant = ["D50 2", "D65 2"]
        self.hexa = hexa
        self.rgb =  self.get_rgb()
        self.hslv =  self.get_hslv()
        self.cmyk =  self.get_cmyk()
        self.xyz =  self.get_xyz()
        self.labuv =  self.get_labuv()
        self.group = self.get_group('rgb')
        self.depth = self.get_depth('rgb')
        
    def get_rgb(self) :
        index = {"r": int(self.hexa[1:3], 16), "g":int(self.hexa[3:5], 16), "b":int(self.hexa[5:7], 16)}
        norm = {"r":float(index['r']/255), "g":float(index['g']/255), "b":float(index['b']/255)}
        maximum = max(index.values())
        minimum = min(index.values())
        sigma = maximum + minimum
        delta = maximum - minimum
        param = {"sum":sum(index.values()), "max":maximum, "min":minimum, "sigma":sigma, "delta":delta}
        # Convert rgb to hsl(rgb)
        x = (2*norm['r']-norm['g']-norm['b'])/2.0
        y = math.sqrt(3.0)*(norm['g']-norm['b'])/2.0
        z = (norm['r'] + norm['g'] + norm['b'])/3.0
        if abs(x)<0.00001 and abs(y)<0.00001 :
            hue = 0
        elif y<0 :
            hue = math.degrees(math.atan2(y,x)) + 360
        else :
            hue = math.degrees(math.atan2(y,x))
        chroma = math.sqrt(x*x + y*y)
        if z<0.00001 or z>0.99999 :
            saturation = 0
        else : 
            saturation = chroma / z
        # Convert to RGB Sphere
        longditude = hue
        if longditude >= 180 :
            longditude = hue - 360
        latitude = math.degrees(math.asin(2*z-1))
        radius = 2 * max([abs(norm['r']-0.5), abs(norm['g']-0.5), abs(norm['b']-0.5)])
        # results
        hsl = {"h": hue, "s": saturation, "l":z, "c": chroma}
        sphere = {"long": longditude, "lati": latitude, "r": radius}
        rgb = {"index": index, "norm": norm, "param": param, "hsl": hsl, "sphere": sphere}
        return rgb

    def get_hslv(self) :
        r = self.rgb['index']['r']
        g = self.rgb['index']['g']
        b = self.rgb['index']['b']
        maximum = self.rgb['param']['max']
        sigma = self.rgb['param']['sigma']
        delta = self.rgb['param']['delta']
        chroma = self.rgb['hsl']['c']
        light = float (sigma / 255) / 2.0
        value = float (maximum / 255)
        if delta == 0 :
            hue = 0
            sl = 0
            sv = 0
        else :
            if maximum ==  r :
                hue = (float((g-b)/delta) % 6) * 60
            elif maximum == g :
                hue = (float((b-r)/delta) % 6 + 2) * 60
            else :
                hue = (float((r-g)/delta) % 6 + 4) * 60
            sl = float(delta/255) / (1 - abs(2*light - 1))
            sv = float(delta/maximum)

        hsl = {"h": hue, "s": sl, "l": light, "c": chroma}
        hsv = {"h": hue, "s": sv, "v": value, "c": chroma}
        hslv = {'hsl': hsl, 'hsv': hsv}
        return hslv

    def get_cmyk(self) :
        k = 1 - self.hslv['hsv']['v']
        if k == 1 :
            c, m, y = 0, 0, 0
        else :
            c = (1 - self.rgb['norm']['r'] - k) / (1 - k)
            m = (1 - self.rgb['norm']['g'] - k) / (1 - k)
            y = (1 - self.rgb['norm']['b'] - k) / (1 - k)
        cmyk = {"c": c, "m": m, "y": y, "k": k}
        return cmyk

    def get_xyz(self) :
        R = self.rgb['norm']['r']
        G = self.rgb['norm']['g']
        B = self.rgb['norm']['b']
        xyz = {}
        for profile in self.profile :
            if profile == "sRGB" :
                X = 0.4124564*R + 0.3575761*G + 0.1804375*B
                Y = 0.2126729*R + 0.7151522*G + 0.0721750*B
                Z = 0.0193339*R + 0.1191920*G + 0.9503041*B
            elif profile == "Adobe RGB" :
                X = 0.5767309*R + 0.1855540*G + 0.1881852*B
                Y = 0.2973769*R + 0.6273491*G + 0.0752741*B
                Z = 0.0270343*R + 0.0706872*G + 0.9911085*B
            elif profile == "CIE RGB" :
                X = 0.4887180*R + 0.3106803*G + 0.2006017*B
                Y = 0.1762044*R + 0.8129847*G + 0.0108109*B
                Z = 0.0000000*R + 0.0102048*G + 0.9897952*B
            sum = X + Y + Z
            if sum == 0 :
                x, y = 0, 0
            else :
                x, y = X / sum, Y / sum
            index = {"X": X, "Y": Y, "Z": Z, "I": sum/3, "x": x, "y": y}
            xyz.update ({profile: index})
        return xyz

    def get_labuv(self) :
        labuv = {}
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
                lab = {"l":L, "a": a, "b": b, "h": H_lab, "s": S_lab, "c": C_lab}
                luv = {"l":L, "u": ua, "v": va, "h": H_luv, "s": S_luv, "c": C_luv}    
                labuv.update({title: {'lab': lab, 'luv': luv}})
        return labuv

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

