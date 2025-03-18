from flask import Flask, render_template, request
from pathlib import Path
import importlib
import drawBot
from defcon import Font
from ufo2ft import compileTTF
from io import BytesIO
import base64
import tempfile

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
        font_filters.append(
            filter_key
        )  # Use stem to get the filename without extension
    return render_template("index.html", font_filters=font_filters)


@app.route("/filter/<filter_key>", methods=["GET", "POST"])
def font_filter(filter_key):
    context = {}
    font = Font("font.ufo")
    if request.method == "GET":
        return render_template("filter.html", filters_map=filters_map, has_font_output_function="FONT_OUTPUT_FUNCTION" in dir(filters_map[filter_key]))
    elif request.method == "POST":
        preview_string = request.form.get("preview_string")
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
                    font_output_function(font)
                    drawBot.saveImage(temp_file.name)
                    output_image = BytesIO()
                    with open(temp_file.name, "rb") as f:
                        output_image.write(f.read())
                    context["output_image"] = base64.b64encode(output_image.getvalue()).decode("ascii")
        return context


if __name__ == "__main__":
    app.run(debug=True)
