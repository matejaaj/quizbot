import pytesseract
from PIL import Image
import openai
import os

def process_region(region):
    """
    Calculate and return the coordinates of a rectangular region in a normalized order.

    Parameters:
    - region: A tuple containing four elements (x1, y1, x2, y2) that represent the coordinates
      of two opposite corners of a rectangle on the image.

    Returns:
    - A tuple (x1, y1, x2, y2) representing the top-left and bottom-right corners of the rectangle,
      ensuring x1 < x2 and y1 < y2.
    """
    x1 = min(region[0], region[2])
    y1 = min(region[1], region[3])
    x2 = max(region[0], region[2])
    y2 = max(region[1], region[3])
    return x1, y1, x2, y2

def process_image(image):
    """
    Process an image to extract text using Optical Character Recognition (OCR).

    Parameters:
    - image: An instance of PIL's Image class.

    Returns:
    - The extracted text as a string. Returns an empty string and prints an error message if
      an exception occurs during processing.
    """
    try:
        gray_image = image.convert('L')  # Convert image to grayscale
        text = pytesseract.image_to_string(gray_image, lang='eng')  # Extract text
        return text
    except Exception as e:
        print(f"Error in OCR processing: {e}")
        return ""

def get_completion(prompt, client):
    """
    Generate a text completion using OpenAI's GPT model based on the provided prompt.

    Parameters:
    - prompt: A string containing the input text for the model.
    - client: An instance of the openai.Client class, configured with an API key.

    Returns:
    - A string containing the model's response. Returns an error message string if an exception occurs.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return ""

def load_api_key():
    """
    Load the OpenAI API key from environment variables.

    Returns:
    - The OpenAI API key as a string. If the environment variable 'OPENAI_API_KEY' is not set,
      returns "default_api_key_here".
    """
    return os.getenv("OPENAI_API_KEY", "default_api_key_here")
