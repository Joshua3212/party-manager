import urllib.parse

import jinja2
import pdfkit
import qrcode.image.svg

for num in range(1, 600):
    qr_code = qrcode.make(num, image_factory=qrcode.image.svg.SvgImage)
    as_svg = qr_code.to_string(encoding="unicode")

    context = {
        "qr": urllib.parse.quote(as_svg),
        "id": num
    }

    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)

    html_template = "template.html"
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    output_pdf = f"./out/{num}.pdf"
    pdfkit.from_string(output_text, output_pdf, configuration=config, options={
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        "page-height": "700px",
        "page-width": "1000px",
        'no-outline': None
    }, css="style.css")
