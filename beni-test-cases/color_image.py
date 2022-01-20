from colorthief import ColorThief
from scipy.spatial import KDTree
from webcolors import (
    CSS21_HEX_TO_NAMES,
    CSS3_HEX_TO_NAMES,
    hex_to_rgb,
    rgb_to_name
)
import colorgram
from google.cloud import vision
import io
import pandas as pd


def convert_rgb_to_names(rgb_tuple, css_db):
    # a dictionary of all the hex and their respective names in css3
    names = []
    rgb_values = []
    for color_hex, color_name in css_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))

    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'{names[index]}'


def cologram_convert(img_url):
    colors = colorgram.extract(img_url, 8)
    dataset = []
    for c_color in colors:
        color_css_2 = convert_rgb_to_names(c_color.rgb, CSS21_HEX_TO_NAMES)
        color_css_3 = convert_rgb_to_names(c_color.rgb, CSS3_HEX_TO_NAMES)
        dataset.append(tuple((c_color.rgb, c_color.proportion, color_css_2, color_css_3)))
    df = pd.DataFrame(dataset, columns=['RGB', 'PROPORTION', 'COLOR-CSS2', 'COLOR-CSS3'])
    print(df)


def color_thief_convert(img_url):
    color_thief = ColorThief(img_url)
    palette_color = color_thief.get_palette(quality=1)
    dataset = []
    for p_color in palette_color:
        color_css_2 = convert_rgb_to_names(p_color, CSS21_HEX_TO_NAMES)
        color_css_3 = convert_rgb_to_names(p_color, CSS3_HEX_TO_NAMES)
        dataset.append(tuple((p_color, color_css_2, color_css_3)))
    df = pd.DataFrame(dataset, columns=['RGB', 'COLOR-CSS2', 'COLOR-CSS3'])
    print(df)


def vision_api_convert(img_url):
    """Detects image properties in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(img_url, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.image_properties(image=image)
    props = response.image_properties_annotation
    dataset = []
    for color in props.dominant_colors.colors:
        t = (color.color.red, color.color.green, color.color.blue)
        color_css_2 = (convert_rgb_to_names(t, CSS21_HEX_TO_NAMES))
        color_css_3 = (convert_rgb_to_names(t, CSS3_HEX_TO_NAMES))
        dataset.append(tuple((t, color.score, color_css_2, color_css_3)))
    df = pd.DataFrame(dataset, columns=['RGB', 'SCORE', 'COLOR-CSS2', 'COLOR-CSS3'])
    print(df)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def get_color_image(img_url):
    print(img_url)
    print('--------------')
    print('Cologram')
    cologram_convert(img_url)
    print('--------------')
    print('Color Thief')
    color_thief_convert(img_url)
    print('--------------')
    print('Vision Api')
    vision_api_convert(img_url)
    print('--------------')


if __name__ == '__main__':
    #get_color_image('hollister_black_shirt_1.jpg')
    #get_color_image('hollister_black_shirt_2.jpg')
    #get_color_image('hollister_black_shirt_3.jpg')
    #get_color_image('hollister_red_shirt.jpg')
    #get_color_image('hollister_white_shirt.jpg')
    get_color_image('zara_orange_shirt.jpg')
    get_color_image('zara_yellow_shirt.jpg')
    get_color_image('zara_blue_shirt.jpg')
