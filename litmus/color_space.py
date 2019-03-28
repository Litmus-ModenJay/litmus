import math

# Color Vector Conversion & Classification
class CVC():
    @staticmethod
    def hexa_RGB(hexa):
        return tuple(int(hexa[2*i+1:2*i+3], 16) for i in range(0,3))
    @staticmethod
    def hexa_rgb(hexa):
        return tuple(float(int(hexa[2*i+1:2*i+3], 16))/255 for i in range(0,3))
    @staticmethod
    def RGB_rgb(RGB):
        return tuple(float(RGB[i])/255 for i in range(0,3))
    @staticmethod
    def rgb_parameters(rgb):
        summation = sum(rgb)
        maximum = max(rgb)
        minimum = min(rgb)
        sigma = maximum + minimum
        delta = maximum - minimum
        return (summation, maximum, minimum, sigma, delta)
    @staticmethod
    def rgb_HSLrgb(rgb):
        r, g, b = rgb[0], rgb[1], rgb[2]
        x = (2*r-g-b)/2.0
        y = math.sqrt(3.0)*(g-b)/2.0
        z = (r + g + b)/3.0
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
        return (hue, saturation, z, chroma)
    @staticmethod
    def rgb_GEOrgb(rgb):
        HSLrgb= CVC.rgb_HSLrgb(rgb)
        hue = HSLrgb[0]
        z = HSLrgb[2]
        if hue >= 180 :
            longditude = hue - 360
        else:
            longditude = hue
        latitude = math.degrees(math.asin(2*z-1))
        radius = 2 * max([abs(rgb[0]-0.5), abs(rgb[1]-0.5), abs(rgb[2]-0.5)])
        return (latitude, longditude, radius)
    
    @staticmethod
    def rgb_HSLV(rgb):
        r, g, b = rgb[0], rgb[1], rgb[2]
        maximum = max(rgb)
        minimum = min(rgb)
        sigma = maximum + minimum
        delta = maximum - minimum
        light = sigma/2.0
        if delta == 0 :
            hue, sl, sv = 0, 0, 0
        else :
            if maximum ==  r :
                hue = (float((g-b)/delta) % 6) * 60
            elif maximum == g :
                hue = (float((b-r)/delta) % 6 + 2) * 60
            else :
                hue = (float((r-g)/delta) % 6 + 4) * 60
            sl = delta / (1 - abs(2*light - 1))
            if maximum :
                sv = delta/maximum
            else:
                sv = 0
        return (hue, sl, light, sv, maximum, delta)
    @staticmethod
    def rgb_CMYK(rgb):
        r, g, b = rgb[0], rgb[1], rgb[2]
        k = 1 - max(rgb)
        if k == 1 :
            c, m, y = 0, 0, 0
        else :
            c = (1 - r - k) / (1 - k)
            m = (1 - g - k) / (1 - k)
            y = (1 - b - k) / (1 - k)
        return (c, m, y, k)
    @staticmethod
    def rgb_XYZ(rgb, profile):
        r, g, b = rgb[0], rgb[1], rgb[2]
        if profile == "sRGB" :
            X = 0.4124564*r + 0.3575761*g + 0.1804375*b
            Y = 0.2126729*r + 0.7151522*g + 0.0721750*b
            Z = 0.0193339*r + 0.1191920*g + 0.9503041*b
        elif profile == "Adobe RGB" :
            X = 0.5767309*r + 0.1855540*g + 0.1881852*b
            Y = 0.2973769*r + 0.6273491*g + 0.0752741*b
            Z = 0.0270343*r + 0.0706872*g + 0.9911085*b
        elif profile == "CIE RGB" :
            X = 0.4887180*r + 0.3106803*g + 0.2006017*b
            Y = 0.1762044*r + 0.8129847*g + 0.0108109*b
            Z = 0.0000000*r + 0.0102048*g + 0.9897952*b
        sum = X + Y + Z
        if sum == 0 :
            x, y = 0, 0
        else :
            x, y = X / sum, Y / sum
        return (X, Y, X, sum/3, x, y)
    @staticmethod
    def XYZ_Labuv(XYZ, illuminant):
        X, Y, Z = XYZ[0], XYZ[1], XYZ[2]
        if illuminant == "D50 2" :
            Xn, Yn, Zn = 0.966797, 1.0000, 0.825188
        elif illuminant == "D65 2" :
            Xn, Yn, Zn = 0.95047, 1.0000, 1.08883
        xn, yn = Xn / (Xn + Yn + Zn), Yn / (Xn + Yn + Zn)
        un, vn = 4*xn / (-2*xn + 12*yn + 3), 9*yn / (-2*xn + 12*yn + 3)
        if X+Y+Z == 0:
            L = 0.0001
            a, b = 0, 0
            u, v = 0, 0
            ua, va = 0, 0
        else :
            L = (116 * CVC.F(Y/Yn) - 16) / 100
            a = (500 * (CVC.F(X/Xn) - CVC.F(Y/Yn))) / 100
            b = (200 * (CVC.F(Y/Yn) - CVC.F(Z/Zn))) / 100
            u = 4 * X / (X + 15*Y + 3*Z)
            v = 9 * Y / (X + 15*Y + 3*Z)
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
            if L>0.99999:
                L = 0.99999
        else :
            S_lab = C_lab / L
            S_luv = C_luv / L
        return (L, a, b, H_lab, S_lab, C_lab, ua, va, H_luv, S_luv, C_luv)
    
    @staticmethod
    def Labuv_GeoLuv(Labuv):
        hue = Labuv[8]
        z = Labuv[0]
        if hue >= 180 :
            longditude = hue - 360
        else:
            longditude = hue
        latitude = math.degrees(math.asin(2*z-1))
        radius = ((Labuv[0]-1/2)**2 + Labuv[6]**2 + Labuv[7]**2)**(1.0/2.0)
        return (latitude, longditude, radius)

    @staticmethod
    def rgb_GEOluv(rgb, profile, illuminant):
        XYZ = CVC.rgb_XYZ(rgb, profile)
        Labuv = CVC.XYZ_Labuv(XYZ, illuminant)
        GeoLuv = CVC.Labuv_GeoLuv(Labuv)
        return GeoLuv
    
    @staticmethod
    def F(value):
        delta = 6/29
        if value > delta**3.0:
            transform = value**(1.0/3.0)
        else:
            transform = value / 3 / (delta**2.0) + 4 / 29
        return transform
    
    @staticmethod
    def rgb_group(rgb):
        HSL = CVC.rgb_HSLrgb(rgb)
        H, L, C = HSL[0], HSL[2], HSL[3]
        group = ''
        if L > 0.9 :
            group = "white"
        elif L < 0.1 :
            group = "black"
        else :
            if C < 0.1 :
                group = "gray"
            else :
                if H >= 15 and H < 45 :
                    if L >= 0.4 :
                        group = "orange"
                    else :
                        group = "brown"
                elif H >= 45 and H < 75 :
                    group = "yellow"
                elif H >= 75 and H < 105 :
                    if L >= 0.5 :
                        if H >= 90 :
                            group = "green"
                        else :
                            group = "yellow"
                    else :
                        group = "green"
                elif H >= 105 and H < 135 :
                    group = "green"
                elif H >= 135 and H < 165 :
                    if L >= 0.5 :
                        group = "cyan"
                    else :
                        group = "green"
                elif H >= 165 and H < 195 :
                    if L < 0.5 :
                        if H >= 180 :
                            group = "blue"
                        else :
                            group = "green"
                    else :
                        group = "cyan"
                elif H >= 195 and H < 225 :
                    if L >= 0.5 :
                        group = "cyan"
                    else :
                        group = "blue"
                elif H >= 225 and H < 255 :
                    group = "blue"
                elif H >= 255 and H < 285 :
                    if L >= 0.5 :
                        group = "purple"
                    else :
                        group = "blue"
                elif H >= 285 and H < 315 :
                    if L < 0.7 :
                        group = "purple"
                    else :
                        group = "pink"
                elif H >= 315 and H < 345 :
                    if L < 0.7 :
                        if H >= 330 :
                            group = "red"
                        else :
                            group = "purple"
                    else :
                        group = "pink"
                else :
                    if L < 0.7 :
                        group = "red"
                    else :
                        group = "pink"
        return group 
    @staticmethod
    def rgb_depth(rgb) :
        L = CVC.rgb_HSLrgb(rgb)[2]
        depth = ''
        if L >= 0.75 :
            depth = "light"
        elif L >= 0.5 :
            depth = "soft"
        elif L >= 0.25 :
            depth = "deep"
        else :
            depth = "dark"
        return depth
    