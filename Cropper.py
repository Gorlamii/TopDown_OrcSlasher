from PIL import Image
import os
import SETTINGS


def crop_tileset(input_dir, block_size_x, block_size_y, output_dir):
    image = Image.open(input_dir)
    image_width, image_height = image.size

    # Iterate over image in terms of block size
    for y in range(0, image_height, block_size_x):
        # Start at right most corner and move backwards in increments of 16
        for x in range(image_width - block_size_x, -1, - block_size_y):
            # Co-ords of Block
            left = x
            top = y
            right = x + block_size_x
            bottom = y + block_size_y
            # [y-axis, x-axis] region to crop
            crop = image.crop((left, top, right, bottom))

            file_name = f'block[{x},{y}].png'
            full_path = os.path.join(output_dir, file_name)
            # Save cropped image as PNG
            crop.save(full_path)


# If path does not exist make it
if not os.path.exists(SETTINGS.CROP_TILESET_PATH):
    os.makedirs(SETTINGS.CROP_TILESET_PATH)
else:
    print(f'The path:\n"{SETTINGS.CROP_TILESET_PATH}"\nexists.\n')
# Only proceed with method if empty and tileset hasn't been cropped
if os.path.exists(SETTINGS.CROP_TILESET_PATH):
    if len(os.listdir(SETTINGS.CROP_TILESET_PATH)) == 0:
        crop_tileset(SETTINGS.TILESET_PATH, SETTINGS.BLOCK_SIZE_X, SETTINGS.BLOCK_SIZE_Y, SETTINGS.CROP_TILESET_PATH)
        print('Tileset Successfully cropped.')
    else:
        print('Tileset seems to already have been cropped (Requested file location is occupied).\n'
              'Are you using the correct Tileset to crop?\n'
              'Or maybe the path location is incorrect.')

