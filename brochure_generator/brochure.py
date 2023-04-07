import image_generator as ig
import pdfkit
from jinja2 import Environment, FileSystemLoader
import base64
from weasyprint import HTML, CSS
from requests import request


def encode_image(filepath):
    with open(filepath, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode()


def generate_pdf(product_description):
    # Fetch a relevant image using the Unsplash API
    image_stream = ig.fetch_image(product_description)

    if image_stream:
        # Create a Jinja2 environment with the templates directory
        env = Environment(loader=FileSystemLoader('templates'))

        # Load the HTML template
        template = env.get_template("index.html")

        product_name = "Mango Drink"
        product_owner = "Team 11"
        product_desc = "Delicious mango drink from the tropicals"

        # Encode the image as Base64 data
        # image_data = base64.b64encode(image_stream.read()).decode()
        # Get the image data as base64-encoded string
        image_data = encode_image("data/brochure.png")

        # image_data = "data/brochure.png"
        # Render the template with the placeholder values and image data
        html_output = template.render(
            product_name=product_name,
            product_owner=product_owner,
            product_desc=product_desc,
            image_data=image_data
        )

        # print(html_output)
        # Convert HTML to PDF using pdfkit
        # pdfkit.from_string(html_output, 'data/output.pdf', options={"enable-local-file-access": ""})

        # Create a PDF from the HTML using WeasyPrint
        HTML(string=html_output).write_pdf('data/output.pdf',stylesheets=[CSS('templates/style.css')])

        print("Brochure generated successfully!")
    else:
        print("Failed to generate brochure")


if __name__ == "__main__":
    product_description = input("Enter the product description: ")
    generate_pdf(product_description)
