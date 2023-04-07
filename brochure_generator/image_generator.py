import PIL
import os
import openai
import requests
from PIL import Image
from io import BytesIO
import random
import io
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")

os.environ['DYLD_LIBRARY_PATH'] = '/opt/venv/lib/python3.9/site-packages/'






# Get the product description from the user
# product_description = input("Please enter the product description: ")

# List of possible background types
backgrounds = ["white", "black", "gray", "blue", "red", "green", "yellow", "wooden", "marble", "brick"]

# List of possible lighting types
lighting = ["bright", "dim", "warm", "cool", "natural", "artificial"]

# List of possible object types
objects = ["plants", "books", "electronics", "decorative items", "furniture", "kitchenware"]

# List of possible angles
angles = ["front", "back", "side", "top", "bottom"]

# List of possible color schemes
colors = ["monochromatic", "analogous", "complementary", "triadic", "neutral", "pastel", "bright", "dark"]

# List of possible image sizes
sizes = ["small", "medium", "large", "extra-large"]

# List of possible resolutions
resolutions = ["low", "medium", "high"]


def random_background():
    """Return a random background type."""
    return random.choice(backgrounds)


def random_lighting():
    """Return a random lighting type."""
    return random.choice(lighting)


def random_number():
    """Return a random number of objects."""
    return random.randint(1, 5)


def random_objects():
    """Return a random object type."""
    return random.choice(objects)


def random_angle():
    """Return a random angle."""
    return random.choice(angles)


def random_color():
    """Return a random color scheme."""
    return random.choice(colors)


def random_size():
    """Return a random image size."""
    return random.choice(sizes)


def random_resolution():
    """Return a random image resolution."""
    return random.choice(resolutions)


# List of possible taglines
taglines = [
    "The ultimate solution for all your needs.",
    "Experience the difference with our innovative product.",
    "Effortlessly elevate your life with our product.",
    "Unlock the full potential of your day with our product.",
    "Designed with your comfort in mind.",
    "Experience the future of technology with our product.",
    "Get more out of life with our innovative product.",
    "Upgrade your lifestyle with our product.",
    "Maximize your potential with our product.",
    "Join the revolution with our innovative product."
]


def random_tagline():
    """Return a random tagline."""
    return random.choice(taglines)


def fetch_image(product_description):
    # Generate an image using DALL·E
    response = openai.Image.create(
        prompt=f"Create an advert image of a product with the following description: {product_description}. "
               f"The product should be placed on a {random_background()} background and should have a {random_lighting()} lighting. "
               f"The image should also include {random_number()} {random_objects()} in the background to provide context. "
               f"The product should be shown in {random_angle()} angle and should have a {random_color()} color scheme. "
               f"The image should be {random_size()} in size and should have a {random_resolution()} resolution."
               f"The image should not contain any text.",
        n=2,
        size="1024x1024",
        response_format="url"
    )

    # Get the image URL from the API response
    image_url = response['data'][0]['url']
    # image_url = response.url
    image_data = requests.get(image_url).content

    # Download the image and save it to a file
    # filename = response.filename

    with open("data/brochure.png", "wb") as f:
        f.write(image_data)

    # # Open the image using PIL and display it
    # advert_image = Image.open("brochure_img.png")
    # # advert_image.show()
    # return advert_image
    pil_image = PIL.Image.open(io.BytesIO(image_data))
    return pil_image




# export DYLD_LIBRARY_PATH=/Users/charusingh/Library/Python/3.11/lib/python/site-packages:$DYLD_LIBRARY_PATH

