from flask import Flask, render_template, request
from pathlib import Path
import importlib
import drawBot
from defcon import Font
from ufo2ft import compileTTF
from io import BytesIO
import base64
import tempfile
import extractor
from fontTools.ttLib import TTFont

base = Path(__file__).parent
app = Flask(__name__)

from filters import *

filters_map = {
    "filter_1": filter_1,
}

def extract_glyphs(tt_font, glyph_names_to_process, ufo):
    """Extract glyph data for the UFO"""
    cmap_reversed = {}
    for k, v in tt_font.getBestCmap().items():
        cmap_reversed.setdefault(v, []).append(k)
    glyph_set = tt_font.getGlyphSet()
    for glyph_name in set(glyph_names_to_process):
        if glyph_name in glyph_set and glyph_name not in ufo:
            glyph = ufo.newGlyph(glyph_name)
            glyph.unicodes = cmap_reversed.get(glyph_name, [])
            pen = glyph.getPen()
            glyph_set_glyph = glyph_set[glyph_name]
            glyph_set_glyph.draw(pen)
            glyph.width = glyph_set_glyph.width


def extract_font_info(tt_font, ufo):
    ufo.info.ascender = tt_font["hhea"].ascent
    ufo.info.descender = tt_font["hhea"].descent
    ufo.info.xHeight = tt_font["OS/2"].sxHeight
    ufo.info.capHeight = tt_font["OS/2"].sCapHeight
    ufo.info.unitsPerEm = tt_font["head"].unitsPerEm  

@app.route("/")
def index():
    font_filters = []
    for filter_key in filters_map:
        font_filters.append(
            filter_key
        )  # Use stem to get the filename without extension
    return render_template("index.html", font_filters=font_filters)


@app.route("/filter/<filter_key>", methods=["GET", "POST"])
def font_filter(filter_key):
    context = {}
    if request.method == "GET":
        return render_template("filter.html", font_filters=filters_map, has_font_output_function="FONT_OUTPUT_FUNCTION" in dir(filters_map[filter_key]))
    elif request.method == "POST":
        tt_font = TTFont(request.files["font_file"])
        font = Font()
        preview_string = request.form.get("preview_string")
        extract_glyphs(tt_font, preview_string, font)
        extract_font_info(tt_font, font)
        filter_module = filters_map[filter_key]
        font_output_function = getattr(filter_module, "FONT_OUTPUT_FUNCTION", None)
        if font_output_function:
            output_font = Font()
            for character in preview_string:
                output_glyph = output_font.newGlyph(character)
                output_glyph.unicode = font[character].unicode
                output_glyph.width = font[character].width
                filter_applied = font_output_function(font[character])
                filter_applied.drawToPen(output_font[character].getPen())
            compiled_ttf = compileTTF(output_font)
            bytes_output = BytesIO()
            compiled_ttf.save(bytes_output)
            base64_output = base64.b64encode(bytes_output.getvalue()).decode("ascii")
            context["output_font"] = base64_output
        else:
            font_output_function = getattr(filter_module, "IMAGE_OUTPUT_FUNCTION", None)
            with drawBot.drawing():
                with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
                    font_output_function(font, preview_string)
                    drawBot.saveImage(temp_file.name)
                    output_image = BytesIO()
                    with open(temp_file.name, "rb") as f:
                        output_image.write(f.read())
                    context["output_image"] = base64.b64encode(output_image.getvalue()).decode("ascii")
        return context


if __name__ == "__main__":
    app.run(debug=True)
