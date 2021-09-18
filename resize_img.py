"""
This script resize each image in testing_photo into 342 * 228
"""

from PIL import Image

NUM_OF_FILES = 200


def main():
    for i in range(21108, 25640):
        str_i = str(i)
        while len(str_i) < 8:
            str_i = '0' + str_i
        # how_many_0s = 7 - i // 10
        # file_name = 'testing_photo/' + str_i + '.jpg'
        file_name = 'valid_4500/' + str_i + '.jpg'

        image = find(file_name)
        if image == 0:
            pass
        else:

            image = Image.open(file_name)
            new_file_name = str_i + '.jpg'
            new_image = image.resize((342, 228))
            new_image.save(new_file_name)


def find(filename):
    try:
        image = Image.open(filename)
        return image
    except FileNotFoundError:
        return 0


if __name__ == '__main__':
    main()