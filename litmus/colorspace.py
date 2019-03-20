import math

# Color Vector Conversion & Classification
class CVC():
    @staticmethod
    def hexa_RGB(hexa):
        return tuple(int(hexa[i+1:i+3], 16) for i in range(0,3))
    @staticmethod
    def hexa_rgb(hexa):
        return tuple(float(int(hexa[i+1:i+3], 16)/255) for i in range(0,3))
    @staticmethod
    def RGB_rgb(RGB):
        return tuple(float(RGB[i]/255) for i in range(0,3))
    @staticmethod
    def RGB_parameters(RGB):
        summation = sum(RGB)
        maximum = max(RGB)
        minimum = min(RGB)
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
        return (longditude, latitude, radius)
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
            sv = delta/maximum
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