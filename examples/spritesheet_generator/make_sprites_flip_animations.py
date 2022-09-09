import math
from typing import List

from PIL import Image, ImageDraw, ImageFont
import numpy

tile_width, tile_height = (48, 100)
#background_color = (73, 109, 137)
tile_color = (90, 90, 90)
font_color = (255, 255, 255)
padding_size = 8
transparency_color = (0, 255, 0)
background_color = transparency_color

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def find_top_half_coeffs_inputs_for_angle(img, angle):
    x_val = (angle * padding_size) / 90
    y_val = min((angle * (img.height)) / 90, img.height - 1)
    # first_list = [(0, y_val), (img.width, y_val), (img.width, img.height), (0, img.height)]
    # print(f"({x_val}, {y_val})")
    # second_list = [(x_val + 1, 0), (img.width - x_val, 0), (img.width, img.height), (0, img.height)]

    first_list = [(-(x_val + 1), y_val), (img.width+x_val, y_val), (img.width, img.height), (0, img.height)]
    second_list = [(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)]
    return first_list, second_list

def find_bottom_half_coeffs_inputs_for_angle(img, angle):
    x_val = ((90-angle) * padding_size) / 90
    y_val = min((angle * (img.height)) / 90, img.height - 1)
    # print(f"(x: {x_val}, y: {y_val})")
    first_list = [(0, 0), (img.width, 0), (img.width+x_val, y_val), (-(x_val + 1), y_val)]
    second_list = [(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)]
    return first_list, second_list

def get_top_half(img):
    top_half = img.crop((0, 0, img.width, img.height // 2))
    return top_half

def get_bottom_half(img):
    bottom_half = img.crop((0, img.height//2, img.width, img.height))
    return bottom_half


def make_sprite(character, font_size=44):
    border_rect_size = (tile_width - padding_size, tile_height - padding_size)
    # inner_image_size = (border_rect_size[0] + 1, border_rect_size[1] + 1)
    inner_image_size = (tile_width, tile_height)
    border_shape = ((padding_size, padding_size), border_rect_size)

    fnt = ImageFont.truetype('LeagueSpartan-Regular.ttf', font_size)
    img = Image.new('RGBA', (tile_width, tile_height), color=background_color)
    d = ImageDraw.Draw(img)

    inner_img = Image.new('RGBA', inner_image_size, color=background_color)

    inner_draw = ImageDraw.Draw(inner_img)
    # inner_draw.rectangle((0, 0, inner_image_size[0], inner_image_size[1]), fill=(100, 100, 200))

    inner_draw.rectangle(border_shape, outline=tile_color, fill=tile_color)

    w, h = inner_draw.textsize(character, font=fnt)
    inner_draw.text((((inner_image_size[0] - w) // 2) - 1, ((inner_image_size[1] - h) // 2) - 1), character,
                    fill=font_color, font=fnt)

    img.paste(inner_img, (padding_size // 2, padding_size // 2))

    inner_img.save("test_inner.png")


    # coeffs = find_coeffs(
    #     [(0, 0), (top_half_inner.width, 0), (top_half_inner.width, top_half_inner.height), (0, top_half_inner.height)],
    #     #[(40, -50), (inner_image_size[0] - 40, -50), (inner_image_size[0], inner_image_size[1]),(0, inner_image_size[1])])
    #     [(padding_size+1, -50), (top_half_inner.width -padding_size, -50), (top_half_inner.width, top_half_inner.height), (0, top_half_inner.height)])

    # coeffs = find_coeffs(
    #     [(0, 25), (top_half_inner.width, 25), (top_half_inner.width, top_half_inner.height), (0, top_half_inner.height)],
    #     [(padding_size + 1, 0),
    #      (top_half_inner.width - padding_size, 0),
    #      (top_half_inner.width, top_half_inner.height),
    #      (0, top_half_inner.height)],
    # )
    #
    # this_angle_img = top_half_inner.transform((top_half_inner.width, top_half_inner.height), Image.PERSPECTIVE, coeffs,
    #                                           Image.BICUBIC)
    # this_angle_img.save(f"top_half_inner.png")
    return inner_img

def make_angles_sprite_set(img, count=10, bottom_skew=False):
    angled_sprites = []
    # test_sheet = Image.new('RGBA', (img.width * 5, img.height * 2), color=(0, 255, 0))
    # test_sheet.save("before_anything.png")

    angle_count_by = (90 // count)+1
    for i, _angle in enumerate(range(0, 91, angle_count_by)):
        #print(f"angle: {_angle}")
        if bottom_skew:
            coeffs = find_coeffs(
                *find_bottom_half_coeffs_inputs_for_angle(img, _angle + 1)
            )
        else: # top skew:
            coeffs = find_coeffs(
                *find_top_half_coeffs_inputs_for_angle(img, _angle + 1)
            )

        this_angle_img = img.transform((img.width, img.height), Image.PERSPECTIVE,
                                                  coeffs,
                                                  Image.BICUBIC)

        #this_angle_img.save(f"test_out/top_half_inner_{_angle + 1}.png")
        coords = (((i % 5) * img.width), ((i // 5) * img.height))
        #print(coords)
        angled_sprites.append(this_angle_img)

        # test_sheet.paste(this_angle_img, coords)
    # test_sheet = test_sheet.convert(mode="P", palette=Image.WEB)
    # test_sheet.save("test_sheet.bmp")
    return angled_sprites

def make_static_sheet(font_size=44):
    full_sheet_img = Image.new("RGBA", (tile_width * 3, tile_height * 4), color=background_color)

    for i in range(10):
        img = make_sprite(f"{i}", font_size=44)
        # img.save(f'char_sprites/pil_text_{i}.png')
        coords = (((i % 3) * tile_width), ((i // 3) * tile_height))
        #print(coords)
        full_sheet_img.paste(img, coords)

    img = make_sprite(f":", font_size=44)
    coords = (((10 % 3) * tile_width), ((10 // 3) * tile_height))
    full_sheet_img.paste(img, coords)

    full_sheet_img = full_sheet_img.convert(mode="P", palette=Image.WEB)
    full_sheet_img.save("static_sheet.bmp")


def pack_images_to_sheet(images, width: int):

    row_count = math.ceil(len(images) / width)

    _img_width = images[0].width
    _img_height = images[0].height
    print(f"len: {len(images)} width:{width} img_w:{_img_width} img_h:{_img_height}")
    _sheet_img = Image.new("RGBA", (_img_width * width, _img_height * row_count), color=transparency_color)
    #_sheet_img.save("before_things.bmp")
    for i, image in enumerate(images):
        coords = (((i % width) * tile_width), ((i // width) * image.height))
        print(coords)
        _sheet_img.paste(image, coords, image)
        #image.save(f"test_out/img_{i}.png")

    return _sheet_img
make_static_sheet(font_size=44)
# make_sheet(font_size=44)

# test_img = make_sprite("2", font_size=44)
# test_img.save('test_image.png')


def make_animations_sheets(font_size=44):

    bottom_sprites = []
    top_sprites = []

    for i in range(10):
        img = make_sprite(f"{i}", font_size=font_size)
        top_half = get_top_half(img)
        bottom_half = get_bottom_half(img)

        bottom_angled_sprites = make_angles_sprite_set(bottom_half, 10, bottom_skew=True)
        top_angled_sprites = make_angles_sprite_set(top_half, 10, bottom_skew=False)

        bottom_sprites.extend(bottom_angled_sprites)
        top_sprites.extend(top_angled_sprites)




    bottom_sheet = pack_images_to_sheet(images=bottom_sprites, width=10)
    #bottom_sheet.save("test_bottom_sheet.png")

    bottom_sheet = bottom_sheet.convert(mode="P", palette=Image.WEB)
    bottom_sheet.save("bottom_animation_sheet.bmp")

    top_sheet = pack_images_to_sheet(images=top_sprites, width=10)
    top_sheet = top_sheet.convert(mode="P", palette=Image.WEB)
    top_sheet.save("top_animation_sheet.bmp")


make_animations_sheets(font_size=44)


# for i, sprite in enumerate(bottom_angled_sprites):
#     sprite.save(f'test_out/bottom_half_{i}.png')
#
# for i, sprite in enumerate(top_angled_sprites):
#     sprite.save(f'test_out/top_half_{i}.png')