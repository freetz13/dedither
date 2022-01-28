from PIL import Image

__version__ = '0.1.0'


def blank_from(image: Image) -> Image:
    return Image.new(mode=image.mode, size=image.size, color=(0, 0, 0, 0))


def get_neighbours(image: Image, coords: tuple) -> list:
    x, y = coords
    result = []
    # right
    if x < image.width - 1:
        result.append(image.getpixel((x+1, y)))
    # left
    if x > 0:
        result.append(image.getpixel((x-1, y)))
    # top
    if y > 0:
        result.append(image.getpixel((x, y-1)))
    # bottom
    if y < image.height - 1:
        result.append(image.getpixel((x, y+1)))
    return result


def blend_pixels(pixels) -> tuple:
    return tuple(
        sum(i)//len(i)
        for i in zip(*pixels)
    )


def chess_split(image: Image) -> tuple:
    whites = blank_from(image)
    blacks = blank_from(image)
    whites_filtered = blank_from(image)
    blacks_filtered = blank_from(image)

    for x in range(image.width):
        for y in range(image.height):
            coordinates = (x, y)
            old_pixel = image.getpixel(coordinates)
            new_pixel = blend_pixels(get_neighbours(image, coordinates))
            # Krinsan's magic
            if (x % 2) == (y % 2):
                whites.putpixel(coordinates, old_pixel)
                whites_filtered.putpixel(coordinates, old_pixel)
                blacks_filtered.putpixel(coordinates, new_pixel)
            else:
                blacks.putpixel(coordinates, old_pixel)
                blacks_filtered.putpixel(coordinates, old_pixel)
                whites_filtered.putpixel(coordinates, new_pixel)
    return whites, blacks, whites_filtered, blacks_filtered
