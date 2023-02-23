"""
Core idea: Generate x cards with ids from 1 to x and apply funky styling.
The cards will be stored in ./cards (hopefully :)
"""
import random
import time
import urllib.parse

import html2image
import jinja2
import qrcode.image.svg

tickets_to_gen = 3
bg_gradients = [
    "linear-gradient( to right top, black, blue)",
    "linear-gradient( to left bottom, black, green)",
    "linear-gradient( to right bottom, black, yellow)",
]

for i in range(1, tickets_to_gen + 1):
    qr_code = qrcode.make(i, image_factory=qrcode.image.svg.SvgImage)
    as_svg = qr_code.to_string(encoding="unicode")
    context = {
        "qr": urllib.parse.quote(as_svg),
        "id": i,
        "created": int(time.time()),
        "bg_gradient": bg_gradients[random.randint(0, 2)]
    }

    fs = jinja2.FileSystemLoader("./")
    jinja2.Environment(loader=fs)

    template = jinja2.Environment(loader=fs).get_template("template.html")
    output_html = template.render(context)
    # print(output_html)
    html2image.Html2Image(size=(1100, 900)).screenshot(html_str=output_html, save_as=f"{i}.png")
