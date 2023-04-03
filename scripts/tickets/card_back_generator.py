import jinja2
import pdfkit

context = {}
template_loader = jinja2.FileSystemLoader("./")
template_env = jinja2.Environment(loader=template_loader)

html_template = "card_back.html"
template = template_env.get_template(html_template)
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
output_pdf = f"./out/card_back.pdf"
pdfkit.from_string(output_text, output_pdf, configuration=config, options={
    'margin-top': '0in',
    'margin-right': '0in',
    'margin-bottom': '0in',
    'margin-left': '0in',
    "page-height": "29.7cm",
    "page-width": "21cm",
    'no-outline': None
})
