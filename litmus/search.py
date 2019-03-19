from .litmus import Litmus
from .color import ColorIndex

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

