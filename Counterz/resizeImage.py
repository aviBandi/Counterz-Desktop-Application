from PIL import Image
import cv2
import math
# Open the image

def resize(inputImagepath, scaleNumberWidth, scaleNumberHeight):

    input_image_path = inputImagepath
    output_image_path = inputImagepath

    # Open the image file
    image = Image.open(input_image_path)

    # Define the size multiplier (e.g., 2 for doubling the size)
    size_multiplier_width = scaleNumberWidth
    size_multiplier_height = scaleNumberHeight

    # Calculate the new size
    width, height = image.size
    
    new_width = int(width * size_multiplier_width)
    new_height = int(height * size_multiplier_height)


    # Resize the image
    resized_image = image.resize((new_width, new_height))

    # Save the resized image
    resized_image.save(output_image_path)

    # Close the image file (optional but recommended)
    image.close()

originalWidth = cv2.imread("firstFrame.png").shape[1]
maskWidth = cv2.imread("images/mask.png").shape[1]
widthscale = originalWidth/maskWidth

originalHeight = cv2.imread("firstFrame.png").shape[0]
maskHeight = cv2.imread("images/mask.png").shape[0]
heightscale = originalHeight/maskHeight

resize("images/mask.png", widthscale, heightscale)
