from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import os
from enum import Enum
from icecream import ic
from datetime import datetime

IS_RELEASE = False

class FILTER(Enum):
    BLUR = 0
    CONTOUR = 1
    DETAIL = 2
    EDGE_ENHANCE = 3
    EDGE_ENHANCE_MORE = 4
    EMBOSS = 5
    FIND_EDGES = 6
    SHARPEN = 7
    SMOOTH = 8
    SMOOTH_MORE = 9