#    Pyamp - Minimal MPD client written in Python using Qt
#    Copyright (C) 2024  Ignacio Gonsalves
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import os
import base64
import sys


def image_to_base64(image_path):
    '''Converts given image to base 64'''
    # Read the image file in binary mode
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Encode the binary data as base64
    base64_string = base64.b64encode(image_data).decode('utf-8')

    return base64_string


# Writes image string to file
def convert_images_to_base64(directory, output_file):
    '''Runs the image_to_base64 func and writes the strings to a file''' 
    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as f:
        # Traverse the directory
        for root, dirs, files in os.walk(directory): # pylint: disable=W0612
            for file in files:
                # Check if the file is an image (you can adjust the extensions as needed)
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Construct the full path to the image file
                    image_path = os.path.join(root, file)

                    # Convert the image to base64
                    base64_string = image_to_base64(image_path)

                    # Write the filename without extension
                    filename_without_extension = os.path.splitext(file)[0].upper()
                    f.write(f'{filename_without_extension} = """\n')

                    # Write the base64 string
                    f.write(f'{base64_string}\n')

                    # Close the string
                    f.write('"""\n\n')


def main():
    '''Runs the script'''
    # Check if directory argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_directory>")
        sys.exit(1)

    # Directory containing the images
    image_directory = sys.argv[1]

    # Output file for storing base64 strings
    output_file = 'images.py'

    # Convert images to base64 and write to a single file
    convert_images_to_base64(image_directory, output_file)


if __name__ == '__main__':
    main()
