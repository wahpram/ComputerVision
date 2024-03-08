import math
from PIL import Image

def rotate_point(x, y, angle):
    radians = math.radians(angle)
    x_prime = x * math.cos(radians) - y * math.sin(radians)
    y_prime = x * math.sin(radians) + y * math.cos(radians)
    return x_prime, y_prime

def rotate_image(input_path, output_path, angle):
    # Open the image file
    image = Image.open(input_path)
    width, height = image.size

    # Create a new blank image to store the rotated result
    rotated_image = Image.new("RGB", (width, height))

    # Iterate through each pixel in the original image
    for x in range(width):
        for y in range(height):
            # Apply rotation to each pixel
            x_prime, y_prime = rotate_point(x - width / 2, y - height / 2, angle)
            x_prime += width / 2
            y_prime += height / 2

            # Ensure the rotated coordinates are within the image bounds
            if 0 <= x_prime < width and 0 <= y_prime < height:
                rotated_image.putpixel((x, y), image.getpixel((int(x_prime), int(y_prime))))

    # Save the rotated image
    rotated_image.save(output_path)

# Example usage:
input_path = "Mini.jpg"
output_path = "output_rotated_image.jpg"
rotation_angle = 90  # Specify the angle by which you want to rotate the image

rotate_image(input_path, output_path, rotation_angle)