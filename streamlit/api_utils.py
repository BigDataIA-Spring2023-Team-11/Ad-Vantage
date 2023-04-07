import base64
import os
import random
import boto3
import openai
import requests
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
openai.api_key = os.environ.get("OPEN_API_ACCESS_KEY")
s3 = boto3.client('s3',region_name='us-east-1',
                             aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                             aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

s3_resource = boto3.resource('s3',
                             region_name='us-east-1',
                             aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),
                             aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))
bucket_name = os.environ.get("SOURCE_BUCKET")
def get_grammer_corrected_text(input_text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Correct this to standard English:\n\n{input_text}",
    temperature=0,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )

  # Extract the generated text from the API response
  grammer_corrected_text = response.choices[0].text
  return grammer_corrected_text


def keyword_generator(input_text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Extract keywords from this text:\n\n{input_text}",
    temperature=0.5,
    max_tokens=200,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
  )
  keywords = response.choices[0].text
  return keywords

def product_name_generator(product_description,adjectives):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Product description: {product_description}\nSeed words: {adjectives}\nProduct names:",
    temperature=0.8,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  products_names = response.choices[0].text
  return products_names


def get_answers1():
  responses = []
  questions = ["Can you summarize what the speaker said?", "What was the main point of the conversation?", "Was there anything surprising or unexpected in the conversation?"]
  for q in questions:
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are filling out a questionnaire."},
        {"role": "user", "content": q}
      ]
    )
    answer = response.choices[0].text.strip()
    responses.append(answer)

  return responses


#-----------------------------------------------------------------------------------

# Define function to generate ad based on user input

def ad_from_product_description(target_audience,product_description):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Write a creative ad for the following product to run on Facebook aimed at {target_audience}:\n\nProduct: {product_description}",
    temperature=0.5,
    max_tokens=100,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
  )
  ad = response.choices[0].text.strip()
  return ad
#-----------------------------------------------------------------------------------

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


def generate_image(product_description,chosen_title):
  # Generate an image using DALL·E
  try:
    response = openai.Image.create(
      prompt=f"Create an advertisement image of a product with the following description: {product_description}. "
             f"The product should be placed on a {random_background()} background and should have a {random_lighting()} lighting. "
             f"The image should also include {random_number()} {random_objects()} in the background to provide context. "
             f"The product should be shown in {random_angle()} angle and should have a {random_color()} color scheme. "
             f"The image should be {random_size()} in size and should have a {random_resolution()} resolution."
             f"Do not include any text in advert image or include the exact {chosen_title}",
      n=1,
      size="1024x1024",
      response_format="url"
    )

    # Get the image URL from the API response
    image_url = response['data'][0]['url']

    # Download the image and save it to a file
    image_data = requests.get(image_url).content
    # Create directory if it doesn't exist
    if not os.path.exists('generated_images'):
      os.makedirs('generated_images')

    with open(f"generated_images/{chosen_title}.png", "wb") as f:
      f.write(image_data)
    send_file_to_s3(f"generated_images/{chosen_title}.png",bucket_name,f"generated_images/{chosen_title}.png")
    # s3_resource.upload_file(f"generated_images/{chosen_title}.png", f"{bucket_name}", f"{chosen_title}.png")

    # Open the image using PIL and return it
    return Image.open(f"generated_images/{chosen_title}.png")

  except Exception as e:
    print(f"Error generating image: {str(e)}")
    return None
#---------------------------------


# # Define the HTML template with placeholders for the product title and description
# if st.button("generate_html"):
"""
take title, product description and image directory as inputs
and consumes html template from s3 bucket which can be modified if required
and adds our product details to it, then uploads to a dir inour s3 bucket
"""
def generate_html(chosen_title,ad_from_api,image_dir):
        # Read the HTML template from S3
    html_template = read_html_template_from_s3("template")
    # Replace the placeholders in the HTML template with the product title and description
    html = html_template.format(
        product_title=chosen_title,
        product_description=ad_from_api,
        image_path=f"{image_dir}"  # {chosen_title}.png
    )
    # Upload the HTML to S3
    try:
        # send_file_to_s3(f"generated_html/{chosen_title}.html", bucket_name, f"generated_html/{chosen_title}.html")
        # s3_resource.put_object(Body=html, Bucket=bucket_name, Key=f"generate_html/{chosen_title}.html", ContentType='text/html')

        s3_resource.Bucket(bucket_name).put_object(Key=f'generated_html/{chosen_title}.html', Body=html)
    except NoCredentialsError:
        return "AWS credentials not available"

    # Return the HTML
    return html
#-----------------------------------------

"""
gets .html file from s3 bucket and reads the content and create a hyper link to return 
"""
def download_html(chosen_title, bucket_name):
    # Download the HTML file from S3
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=f'generated_html/{chosen_title}.html')
    html_contents = response['Body'].read().decode('utf-8')

    # Create a download link for the HTML file
    b64 = base64.b64encode(html_contents.encode()).decode()
    href = f'<a href="data:file/html;base64,{b64}" download="{chosen_title}.html">Download file</a>'

    return href

#-----------------------------------------------------------------------------------
def send_file_to_s3(file_path, s3_bucket, s3_key):
    """
    Uploads a file to S3

    :param file_path: Path to the file to upload
    :param s3_bucket: Name of the S3 bucket to upload the file to
    :param s3_key: Key to use when storing the file in S3
    """
    with open(file_path, 'rb') as f:
        s3_object = s3_resource.Object(s3_bucket, s3_key)
        s3_object.upload_fileobj(f)
#-----------------------------------------------------------------------------------

# def get_my_s3_url(filename):
#     static_url = f"https://{bucket_name}.s3.amazonaws.com"
#     filename_alone = filename.split("/")[-1]
#     generated_url = f"{static_url}/generated_images/{filename}"
#     return generated_url
s3_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))

def get_s3_object_url( object_name):
    s3 = boto3.client('s3')
    expiration = 3600  # Link expiration time in seconds (1 hour in this case)

    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': bucket_name, 'Key': f"generated_images/{object_name}"},
        ExpiresIn=expiration
    )

    return url

#-----------------------------------------------------------------------------------

def read_html_template_from_s3(filename):
    file_key = f'template/{filename}.txt'

    response = s3.get_object(Bucket=bucket_name, Key=file_key)

    text = response['Body'].read().decode('utf-8')

    return text

#------------------------------------------------------------------------------------
def get_answers():
  responses = []
  questions = ["Can you summarize what the speaker said?",
               "What was the main point of the conversation?",
               "Was there anything surprising or unexpected in the conversation?"]

  # transcript = "Speaker 1: Hi, how are you?\nSpeaker 2: I'm good, thanks for asking. How about you?\nSpeaker 1: I'm doing well, thanks. So, what brings you here today?"
  transcript = "on the work, scraping on the data science, whatever you're web scraping for, you can focus on that. They have a success rate of average 99.2% and the residential proxies offer, as I said, 100 million plus legit IPs from 195 countries. You can also take a look at their quick start. You can use this with curl with a command line tool on Linux on Windows. You can use it for PHP and probably most interesting for you guys, you can use it with Python as well. You can look at the tutorial here to see how it's done. You can specify a server. You can also specify the country, the city. You can do all this manually and these are legitimate IP addresses, reliable service. The company is very reliable. If you go to Reddit and you look for best proxy server."
  for q in questions:
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=f"{transcript}\nQ: {q}\nA:",
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    responses.append(answer)

  return responses


#-----------------------------------------------------------------
