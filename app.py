from flask import Flask, render_template, request
from pathlib import Path
import importlib
import drawBot
from defcon import Font
from ufo2ft import compileTTF
from io import BytesIO
import base64

base = Path(__file__).parent
app = Flask(__name__)

from filters import *

filters_map = {
    "filter_1": filter_1,
}

@app.route("/")
def index():
    font_filters = []
    for filter_key in filters_map:
        font_filters.append(filter_key)  # Use stem to get the filename without extension
    return render_template("index.html", font_filters=font_filters)

@app.route("/filter/<filter_key>", methods=['GET', 'POST'])
def font_filter(filter_key):
    print(request.method)
    context = {}
    if request.method == "GET":
        return render_template("filter.html")

    elif request.method == "POST":
        filter_module = filters_map[filter_key]
        drawing = drawBot.newDrawing()
        font = Font("font.ufo")
        font_output_function = getattr(filter_module, "FONT_OUTPUT_FUNCTION", None)
        drawBot.endDrawing()
        if font_output_function:
            output_font = Font()
            output_glyph = output_font.newGlyph("A")
            output_glyph.unicode = font["A"].unicode
            output_glyph.width = font["A"].width

            filter_applied = font_output_function(font["A"])
            filter_applied.drawToPen(output_font["A"].getPen())
            compiled_ttf = compileTTF(output_font)
            bytes_output = BytesIO()
            compiled_ttf.save(bytes_output)
            base64_output = base64.b64encode(bytes_output.getvalue()).decode("ascii")
            context["output_font"] = base64_output
        else:
            print(drawing)
        return context

if __name__ == "__main__":
    app.run(debug=True)