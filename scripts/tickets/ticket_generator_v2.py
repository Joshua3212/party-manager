import urllib.parse

import jinja2
import pdfkit
import qrcode.image.svg

total_tickets = 600
per_page = 8
current_num = 0


def gen_qr(num: int):
    qr_code = qrcode.make(num, image_factory=qrcode.image.svg.SvgImage)
    as_svg = qr_code.to_string(encoding="unicode")
    return urllib.parse.quote(as_svg)


for i in range(1, int(total_tickets / per_page) + 1):
    # per page
    context = {}
    for x in range(1, per_page + 1):
        current_num += 1
        context[f"id{x}"] = current_num
        context[f"qr{x}"] = gen_qr(current_num)

    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)

    html_template = "template.html"
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
    output_pdf = f"./out/{i}.pdf"
    pdfkit.from_string(
        output_text,
        output_pdf,
        configuration=config,
        options={
            "margin-top": "0in",
            "margin-right": "0in",
            "margin-bottom": "0in",
            "margin-left": "0in",
            "page-height": "29.7cm",
            "page-width": "21cm",
            "no-outline": None,
        },
    )
