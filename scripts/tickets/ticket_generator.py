"""
Core idea: Generate x cards with ids from 1 to x and apply funky styling.
The cards will be stored in ./cards (hopefully :)
"""
import random
import time

import jinja2
import pdfkit

tickets_to_gen = 3
bg_gradients = [
    "linear-gradient(red, blue)",
    "linear-gradient(red, green)",
    "linear-gradient(yellow, blue)",
]

for i in range(1, tickets_to_gen + 1):
    context = {
        "id": i,
        "created": int(time.time()),
        "bg_gradient": bg_gradients[random.randint(0, 2)]
    }

    fs = jinja2.FileSystemLoader("./")
    jinja2.Environment(loader=fs)

    template = jinja2.Environment(loader=fs).get_template("template.html")
    output_html = template.render(context)
    print(output_html)
    output_pdf = pdfkit.from_string(output_html, f"./tickets/{i}.pdf")
