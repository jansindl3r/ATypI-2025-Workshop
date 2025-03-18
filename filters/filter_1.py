from fontPens.flattenPen import FlattenPen
from fontPens.transformPointPen import TransformPointPen 
from fontParts.world import OpenFont
from drawBot import *

font = OpenFont("font.ufo")
glyph = font["A"]

__all__ = ["export_font"]

def circle(pen, center, radius=20, tension=0.55):
    x, y = center
    d = radius * tension
    pen.moveTo((x + radius, y))
    pen.curveTo((x + radius, y + d), (x + d, y + radius), (x, y + radius))
    pen.curveTo((x - d, y + radius), (x - radius, y + d), (x - radius, y))
    pen.curveTo((x - radius, y - d), (x - d, y - radius), (x, y - radius))
    pen.curveTo((x + d, y - radius), (x + radius, y - d), (x + radius, y))
    pen.closePath()
    pen.endPath()
    
def square(pen, center, size=10):
    x, y = center
    pen.moveTo((x + size, y - size))
    pen.lineTo((x + size, y + size))
    pen.lineTo((x - size, y + size))
    pen.lineTo((x - size, y - size))
    pen.closePath()
    pen.endPath()
    
def translate_glyph(pen, offset):
    try:
        offset_x, offset_y = offset
    except TypeError:
        offset_x = offset_y = offset
    output_pen = BezierPath()
    transform_pen = TransformPointPen(output_pen, (1, 0, 0, 1, offset_x, offset_y))
    pen.drawToPointPen(transform_pen)
    return output_pen

def skew_glyph(pen, angle):
    try:
        skew_x, skew_y = angle
    except TypeError:
        skew_x = skew_y = angle
    output_pen = BezierPath()
    transform_pen = TransformPointPen(output_pen, (1, radians(skew_x), radians(skew_y), 1, 0, 0))
    pen.drawToPointPen(transform_pen)
    return output_pen


class BubblePen():
    def __init__(self, other_pen):
        self.other_pen = other_pen
        
    def moveTo(self, point):
        circle(self.other_pen, point)
        
    def lineTo(self, point):
        circle(self.other_pen, point)
    
    def closePath(self):
        self.other_pen.closePath()


def export_font(glyph):
    output_pen = BezierPath()
    flatten_pen = FlattenPen(output_pen, approximateSegmentLength=20)
    bubble_pen = BubblePen(flatten_pen)
    flatten_pen = FlattenPen(bubble_pen, segmentLines=True, approximateSegmentLength=40)
    glyph.draw(flatten_pen)
    drawPath(output_pen)

    for i in range(10):
        fill(i/10)
        translated_pen = translate_glyph(skew_glyph(output_pen, [-i*2, i*2]), i*20)
        drawPath(translated_pen)
    return output_pen

FONT_OUTPUT_FUNCTION = export_font
    
